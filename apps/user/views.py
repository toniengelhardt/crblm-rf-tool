import logging
from datetime import timedelta
from typing import Tuple

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from allauth.account.forms import SignupForm
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from core.email import send_templated_email
from .models import MagicLinkToken, Profile
from .serializers import ProfileSerializer, UserSerializer


logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class SignupView(APIView):
    """Register a new user."""
    permission_classes: Tuple = (AllowAny,)

    def post(self, request: Request, **kwargs) -> Response:
        form = SignupForm(request.data)
        if form.is_valid():

            # Create user and set inactive.
            user = form.save(request)
            user.is_active = False
            # Fix for duplicated emails due to case insensitivity.
            user.email = user.email.lower()
            user.save()

            # Add additional info to profile.
            now = timezone.now()
            profile = user.profile
            profile.terms_accepted_dt = now
            profile.privacy_accepted_dt = now
            profile.save()

            # Send confirmation email.
            protocol = 'http' if settings.DEBUG else 'https'
            current_site = Site.objects.get(id=settings.SITE_ID)
            confirm_url = f'{protocol}://{current_site.domain}/activate/{profile.confirm_token}'

            try:
                subject = 'Confirm your Email'
                delivered_to = send_templated_email(
                    recipients=[user.email],
                    subject=subject,
                    from_email=settings.WELCOME_FROM_EMAIL,
                    text_template='email/confirm_email/email_content.txt',
                    html_template='email/confirm_email/email_content.html',
                    context={
                        'confirm_url': confirm_url,
                    },
                )
                if len(delivered_to) < 1:
                    logger.info(f"Email with subject '{subject}' was not delivered to {user.email}.")
                return Response()
            except Exception as exc:
                msg = f"An error occured when sending a confirmation email to '{user.email}': %{str(exc)}s"
                logger.error(msg)
                return Response(msg, status=500)

        return Response({'errors': form.errors.as_data()}, status=400)


class ActivateAccountView(APIView):
    """Confirms a `User`s email address and activates the account.

    This is only applicable for the local auth strategy.
    """
    permission_classes: Tuple = (AllowAny,)

    def post(self, request: Request, **kwargs) -> Response:
        token = request.data.get('token')
        try:
            User = get_user_model()
            user = User.objects.get(profile__confirm_token=token)
        except ObjectDoesNotExist:
            return Response('Your link is not valid, please contact our support.', status=400)
        # Check if the account has already been activated to avoid logins
        # with an old token.
        # NOTE: just checking if the user is active will not work here because
        # SendGrid executes the link already once. Therefore check the time.
        now = timezone.now()
        profile = user.profile
        if profile.email_verified_on and profile.email_verified_on < now - timedelta(minutes=5):
            raise ValidationError('Your account has been activated, just go to the login page and sign in.')
        user.is_active = True
        user.save()
        profile.email_verified_on = now
        profile.save()

        # Send confirmation email.
        profile.send_welcome_email()

        # Generate a token pair to directly authenticate the user.
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh.token),
        })


class UserView(APIView):
    """Retrieve or delete user."""
    serializer_class = UserSerializer

    def get(self, request: Request, **kwargs) -> Response:
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def delete(self, request: Request, **kwargs) -> Response:
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    """Retrieve and update user profile."""
    serializer_class = ProfileSerializer

    def get_object(self) -> Profile:
        return self.request.user.profile

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        return self.partial_update(request, *args, **kwargs)


class DisconnectProviderView(APIView):
    serializer_class = ProfileSerializer

    def put(self, request: Request, **kwargs) -> Response:
        """Disconnect social provider from profile"""
        try:
            provider = request.data.get('provider', 0)
            request.user.socialaccount_set.filter(provider=provider).delete()
            serializer = self.serializer_class(request.user.profile)
            return Response(serializer.data)
        except ObjectDoesNotExist as exc:
            raise ValidationError('Account does not exist.') from exc


class LogoutView(APIView):
    """Invalidate user tokens (blacklist)

    Important: this will only invalidate the tokens from the current device.
    Other outstanding tokens for the account will stay valid.
    """
    def post(self, request: Request, **kwargs) -> Response:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                outstanding_token = OutstandingToken.objects.get(token=refresh_token)
                BlacklistedToken.objects.get_or_create(token=outstanding_token)
            except ObjectDoesNotExist:
                pass

        return Response()


class ChangePasswordView(APIView):
    """Change account password."""
    def post(self, request: Request, **kwargs) -> Response:
        user = request.user
        password = request.data.get('password')

        try:
            validate_password(password, user)
        except Exception as exc:
            raise ValidationError(str(exc)) from exc

        # Invalidate all refresh tokens of the current user.
        blacklisted_token_ids = BlacklistedToken.objects.filter(token__user=user).values_list('token_id', flat=True)

        for token in OutstandingToken.objects.filter(user=user).exclude(id__in=blacklisted_token_ids):
            BlacklistedToken.objects.create(token=token)

        user.set_password(password)
        user.save()

        return Response()


class MagicLinkView(APIView):
    """Generate an auth/refresh token pair from a Magic Link

    Checks if the token is valid...
    """
    permission_classes: Tuple = (AllowAny,)

    def post(self, request: Request, **kwargs) -> Response:
        # Check if token is valid.
        token = request.data.get('token')
        now = timezone.now()
        min_creation_dt = now - settings.MAGIC_LINK_LIFETIME
        mlt = MagicLinkToken.objects.filter(token=token).first()
        if not mlt:
            raise ValidationError('Invalid link.')
        if mlt.created < min_creation_dt:
            raise ValidationError('Link expired, please request a new link.')
        if mlt.used_dt and (now - mlt.used_dt).seconds > 3:
            # NOTE: For some reason, in production the link is always already
            # used and the POST request is executed twice (maybe due to a
            # Chrome plugin or something like that). Therefore, allow 3 seconds
            # validity for the link from the time it is used first (not sure if
            # this is safe!). Improve later...
            raise ValidationError('Link already used.')
        # Invalidate token.
        mlt.used_dt = now
        mlt.save()
        # Get user and generate token.
        User = get_user_model()
        user = User.objects.get(email__iexact=mlt.email, is_active=True)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })


@method_decorator(csrf_exempt, name='dispatch')
class ResetPasswordView(APIView):
    """Generate a one-time login token and send it via email."""
    permission_classes: Tuple = (AllowAny,)

    def post(self, request: Request, **kwargs) -> Response:
        email = request.data.get('email').lower()
        User = get_user_model()
        if not User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Email not found')

        # Delete existing ML tokens for this email address.
        MagicLinkToken.objects.filter(email=email).delete()

        # Create magic token.
        mlt = MagicLinkToken.objects.create(email=email)

        # Send confirmation email.
        protocol = 'http' if settings.DEBUG else 'https'
        current_site = Site.objects.get(id=settings.SITE_ID)
        magic_url = f'{protocol}://{current_site.domain}/ml/{mlt.token}'

        # Send email natively.
        try:
            subject = 'Reset your password'
            delivered_to = send_templated_email(
                recipients=[email],
                subject=subject,
                from_email=settings.DEFAULT_FROM_EMAIL,
                text_template='email/magic_link/email_content.txt',
                html_template='email/magic_link/email_content.html',
                context={
                    'magic_url': magic_url,
                },
            )
            if len(delivered_to) < 1:
                logger.error(f"Email with subject '{subject}' was not delivered to {email}.")
        except Exception as exc:
            msg = f"An error occured when sending a Magic Link email to '{email}': %{str(exc)}s"
            logger.error(msg)
            return Response(msg, status=500)

        return Response()

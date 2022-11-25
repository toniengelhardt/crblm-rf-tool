from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account has no email or email is unknown, just go on
        - social account's email exists, link social account to existing user

        Source:
        https://stackoverflow.com/questions/19354009/django-allauth-social-login-automatically-linking-social-site-profiles-using-th
        """
        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return

        # Some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, but allauth takes care of this case so just
        # ignore it
        if 'email' not in sociallogin.account.extra_data:
            return

        # Check if given email address already exists.
        # Note: __iexact is used to ignore cases
        User = get_user_model()
        try:
            email = sociallogin.account.extra_data['email'].lower()
            user = User.objects.get(email__iexact=email)

        # ...if it does not, let allauth take care of this new social account
        except User.DoesNotExist:
            return

        # ...if it does, connect this new social login to the existing user
        sociallogin.connect(request, user)

    def save_user(self, request, sociallogin, form):
        user = super().save_user(request, sociallogin, form=form)

        # Accept terms and privacy
        now = timezone.now()
        profile = user.profile
        profile.terms_accepted_dt = now
        profile.privacy_accepted_dt = now
        if user.email:
            profile.email_verified_on = now
        profile.save()

        # Send confirmation email.
        profile.send_welcome_email()

        return user


class SocialRefreshMixin:
    """Fix refresh_tokens for social auth login views

    The allauth views do not have the capability to refresh tokens, hence
    patching with the TokenRefreshSerializer from simple_jwt is required.
    """
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')

        if refresh_token:

            # While allauth uses the keys 'access_token' and 'refresh_token',
            # simple_jwt uses the keys 'access' and 'refresh'. Therefore patching is required.

            # pylint: disable=protected-access

            request.data._mutable = True
            request.data['refresh'] = refresh_token
            request.data._mutable = False

            # pylint: enable=protected-access

            serializer = TokenRefreshSerializer(data=request.data)

            try:
                serializer.is_valid(raise_exception=True)
            except TokenError as exc:
                raise InvalidToken(exc.args[0]) from exc

            data = serializer.validated_data
            data['access_token'] = data.pop('access')

            # The refresh token seems to be only in the dict if the
            # ROTATE_REFRESH_TOKENS setting is set to True in settings.
            if 'refresh' in data:
                data['refresh_token'] = data.pop('refresh')

            return Response(data)

        return super().post(request, *args, **kwargs)


class FacebookLogin(
    SocialRefreshMixin,
    SocialLoginView,
):
    authentication_classes = []
    adapter_class = FacebookOAuth2Adapter
    callback_url = settings.SOCIAL_LOGIN_CALLBACK_URL
    client_class = OAuth2Client


class GoogleLogin(
    SocialRefreshMixin,
    SocialLoginView,
):
    authentication_classes = []
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.SOCIAL_LOGIN_CALLBACK_URL
    client_class = OAuth2Client

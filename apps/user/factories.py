from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from .models import Profile


# Profile example from docs:
# https://factoryboy.readthedocs.io/en/latest/recipes.html#example-django-s-profile


class DisableProfileSignalMixin:
    """
    Needs to be included in all Factories that
    use a ProfileFactory.

    NOTE:
    The factory boy documentation recommends to use
    the mute_signals decorator, but the decorator needs
    to be included on all Factories that use ProfileFactory
    and it turns of ALL post_save signals.
    """
    @classmethod
    def _generate(cls, create, attrs):
        from apps.user.models import user_post_save  # pylint: disable=import-outside-toplevel
        user_model = get_user_model()
        post_save.disconnect(sender=user_model, dispatch_uid='user_post_save')
        user = super()._generate(create, attrs)
        post_save.connect(user_post_save, sender=user_model, dispatch_uid='user_post_save')
        return user


class ProfileFactory(DisableProfileSignalMixin, DjangoModelFactory):
    # We pass in profile=None to prevent UserFactory from creating
    # another profile (this disables the RelatedFactory)
    user = factory.SubFactory('apps.user.factories.UserFactory', profile=None)

    class Meta:
        model = Profile


class UserFactory(DisableProfileSignalMixin, DjangoModelFactory):
    username = factory.Faker('user_name')

    # We pass in 'user' to link the generated UserProfile to our just-generated User.
    # This will call ProfileFactory(user=our_new_user), thus skipping the SubFactory.
    profile = factory.RelatedFactory(ProfileFactory, 'user')

    class Meta:
        model = settings.AUTH_USER_MODEL

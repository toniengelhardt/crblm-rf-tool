import logging
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.socialaccount.models import SocialAccount

from core.models import BaseModel


logger = logging.getLogger(__name__)


class Profile(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=True, blank=True)

    # Standard methods

    def __str__(self) -> str:
        return self.name or self.username

    # Own methods

    @property
    def username(self) -> str:
        return self.user.username

    @property
    def email(self) -> str:
        return self.user.email

    @property
    def active(self) -> str:
        return self.user.is_active

    @property
    def facebook_connected(self):
        return SocialAccount.objects.filter(user=self.user, provider='facebook').exists()

    @property
    def google_connected(self):
        return SocialAccount.objects.filter(user=self.user, provider='google').exists()

    @property
    def provider_list(self):
        return ", ".join([sa.provider for sa in self.user.socialaccount_set.all()])

# User signals.

@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid='user_post_save')
def user_post_save(sender, instance, created, raw, **kwargs):
    """Create Profile when User is created."""
    if created and not raw:
        # Generate profile.
        Profile.objects.create(user=instance)

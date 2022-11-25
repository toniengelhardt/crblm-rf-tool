from django.contrib.auth.models import User  # pylint: disable=imported-auth-user

from rest_framework import serializers

from core.serializers import BaseModelSerializer
from .models import Profile


class ProfileSerializer(BaseModelSerializer):
    account_type_name = serializers.CharField(source='get_account_type_display')
    stripe_customer_id = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'id', 'uid', 'created_sts', 'username', 'email', 'facebook_connected',
            'google_connected', 'account_number', 'account_type', 'account_type_name',
            'pro', 'internal', 'developer', 'beta', 'used_storage_capacity', 'birthday',
            'sync_id', 'sync_sts', 'last_update_sts', 'profile_settings', 'device_settings',
            'stripe_customer_id', 'stripe_active_subscriptions',
        )
        read_only_fields = (
            'uid', 'created_sts', 'username', 'email', 'facebook_connected',
            'google_connected', 'account_number', 'account_type', 'account_type_name',
            'pro', 'internal', 'developer', 'used_storage_capacity', 'sync_id', 'sync_sts',
            'last_update_sts', 'stripe_customer_id', 'stripe_active_subscriptions',
        )

    def get_stripe_customer_id(self, obj):
        return obj.stripe_customer_id


class UserSerializer(BaseModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile',)

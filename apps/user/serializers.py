from django.contrib.auth.models import User

from core.serializers import BaseModelSerializer
from .models import Profile


class ProfileSerializer(BaseModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name',)


class UserSerializer(BaseModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile',)

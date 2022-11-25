from rest_framework.permissions import AllowAny

from core.views import BaseModelViewSet
from .models import Profile
from .serializers import ProfileSerializer


class ProfilesViewSet(BaseModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Profile.objects.all()

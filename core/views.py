from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


class BaseModelViewSet(ModelViewSet):
    """Base model for most ModelViewSets."""
    pass


#   Test views.
# ------------------------------------------------------------------------------

class PingView(APIView):
    """
    Returns 'Pong' response with status code 200 to incoming GET requests.
    Used in tests to initialize get_current_user() or to make sure that the
    API endpoint is working.
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response('Pong')

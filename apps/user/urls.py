from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    ChangePasswordView, DisconnectProviderView, LogoutView, ProfileView,
    ResetPasswordView, UserView,
)


app_name = 'user'


urlpatterns = [
    path('', UserView.as_view(), name='me'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/disconnect-provider/', DisconnectProviderView.as_view(), name='disconnect_provider'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', csrf_exempt(ResetPasswordView.as_view()), name='reset_password'),
]

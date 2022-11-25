from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import PingView


api_urls = ([

    # Checks:
    path('ping/', PingView.as_view()),  # Check if the API works.

    # Authentication:
    # path('auth/signup/', csrf_exempt(SignupView.as_view()), name='signup'),
    # path('auth/mlt/', MagicLinkView.as_view(), name='magic_link'),
    # path('auth/activate/', ActivateAccountView.as_view(), name='activate'),
    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App endpoints:
    path('assessments/', include('apps.assessments.urls')),
])


urlpatterns = [

    # Allauth:
    path('accounts/', include('allauth.urls')),

    # Admin:
    path('admin/', admin.site.urls),

     # API:
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(api_urls)),

    # Authentication:
    path('auth/', include('dj_rest_auth.urls')),
    # path('auth/social/facebook/', FacebookLogin.as_view(), name='facebook_login'),
    # path('auth/social/google/', GoogleLogin.as_view(), name='google_login'),

] + static(settings.MEDIA_URL_PUBLIC, document_root=settings.MEDIA_ROOT + settings.MEDIA_PUBLIC_DIR)


if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]

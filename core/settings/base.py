# pylint: disable=unused-import

import os
from datetime import timedelta

from core.logging import RequireTestingFalse

# Fix outdated packages for Django 4
# https://stackoverflow.com/questions/71589827/i-have-an-error-about-smart-text-after-installing-django-admin-charts

import django  # pylint: disable=wrong-import-order
from django.utils.encoding import smart_str  # pylint: disable=wrong-import-order

django.utils.encoding.smart_text = smart_str

# End fix

TEST = False
DEBUG = False  # Override in local.py
DEBUG_TOOLBAR = True


#   PROTOCOL & DOMAIN
# ----------------------------------------------

HTTP_PROTOCOL = 'https'
WEBSITE_DOMAIN = 'example.com'

WEBSITE_URL = f'{HTTP_PROTOCOL}://{WEBSITE_DOMAIN}'


#   SECURITY
# ----------------------------------------------

# SECURITY WARNING: change this key for production and keep it secret!
SECRET_KEY = 'django-insecure-+e(bxkw*@v-syeu3dx%gu*cqwd7%i=r0(sk*y4-^&900rwt1_a'
ALLOWED_HOSTS = []
INTERNAL_IPS = ['127.0.0.1']


# Application definition
# ----------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'corsheaders',
    'django_filters',
    'django_inlinecss',
    'import_export',
    'pytz',
    'core',
    'apps.assessments',
    'apps.user',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


#   CORS
# ----------------------------------------------

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://[\w-]+\.example\.com$",
]


#   AUTHENTICATION
# ----------------------------------------------

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Allauth:
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True

# Socialauth:
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'FIELDS': [
            'id',
            'email',
            'name',
            'verified',
            'link',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': True,
    },
    'google': {
        'SCOPE': ['email', 'profile'],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'VERIFIED_EMAIL': True,
    }
}

# Disable email verification since this is just a test.
# If you want to enable it, you'll need to configure django-allauth's email confirmation pages
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_REQUIRED = False

# Custom adapter:
# https://stackoverflow.com/questions/19354009/django-allauth-social-login-automatically-linking-social-site-profiles-using-th
SOCIALACCOUNT_ADAPTER = 'core.auth.CustomSocialAccountAdapter'

# NOTE:
# Override this in local settings with smth like http://localhost:8000/login
SOCIAL_LOGIN_CALLBACK_URL = WEBSITE_URL + '/login'


#   FILE SYSTEM & FINDERS
# ----------------------------------------------

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)
ROOT_URLCONF = 'core.urls'

ASGI_APPLICATION = 'core.asgi.application'
WSGI_APPLICATION = 'core.wsgi.application'

# IMPORTANT!!!
# This has to be before the 'Templates' setting.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',  # Put base template and cross-app templates in /templates.
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


#   STATIC & MEDIA FILES
# ----------------------------------------------

# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_PUBLIC_DIR = 'public/'
MEDIA_PROTECTED_DIR = 'protected/'
MEDIA_URL = '/media/'
MEDIA_URL_PUBLIC = MEDIA_URL + MEDIA_PUBLIC_DIR
MEDIA_URL_PROTECTED = MEDIA_URL + MEDIA_PROTECTED_DIR

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


#   SITES
# ----------------------------------------------

SITE_ID = 1


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


#   LOGGING
# ----------------------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_testing_false': {
            '()': RequireTestingFalse,
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'ERROR',
            'filters': ['require_debug_false', 'require_testing_false'],
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', 'require_testing_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': [
                'console',
            ],
        },
        'django.request': {
            'handlers': [
                'file',
                'mail_admins',
            ],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': [
                'file',
                'mail_admins',
            ],
            'level': 'ERROR',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    },
}


#   REST FRAMEWORK
# ----------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

# Use JWT with dj_rest_auth
REST_USE_JWT = True
JWT_AUTH_COOKIE = "jwt-auth"

SIMPLE_JWT = {
    'SIGNING_KEY': SECRET_KEY,
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    'LEEWAY': timedelta(minutes=2),
    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'ROTATE_REFRESH_TOKENS': True, # Rotate the tokens to allow infinite refresh lifetime.
    'BLACKLIST_AFTER_ROTATION': True, # Invalidate refresh token when it is used and rotated.
}


#   OTHER APPS
# ----------------------------------------------

INLINECSS_CSS_LOADER = 'django_inlinecss.css_loaders.StaticfilesFinderCSSLoader'


#   APP SETTINGS
# ----------------------------------------------

SITE_NAME = "Django Nuxt Starter"

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

API_ROOT = '/api'


#   LOAD EMAIL SETTINGS
# ----------------------------------------------
try:
    from .email import *  # pylint: disable=wildcard-import,unused-wildcard-import
except Exception:
    # Output emails to console.
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    print("Could not retrieve email settings, using console output.")


#   LOAD LOCAL SETTINGS
#   NOTE: Everything after this point cannot be overwritten by local settings.
# ----------------------------------------------
try:
    from .local import *  # pylint: disable=wildcard-import,unused-wildcard-import
except ImportError:
    pass


#   DEBUG MODE
# ----------------------------------------------

if DEBUG:
    # Only enable the REST UI in dev mode for security reasons.
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')
    REST_FRAMEWORK['EXCEPTION_HANDLER'] = 'core.utils.debug_exception_handler'

if DEBUG_TOOLBAR:
    INSTALLED_APPS += [
        'django_extensions',
        'debug_toolbar',
    ]
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + MIDDLEWARE
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }

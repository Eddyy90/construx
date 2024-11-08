from os.path import join
from pathlib import Path, os
from django.contrib.messages import constants as messages
from crispy_forms.helper import FormHelper
from dotenv import load_dotenv

load_dotenv()

FormHelper.use_custom_control = False

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
APP_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

# SECURITY WARNING: don't run with debug turned on in production!
PRODUCTION = os.getenv("PRODUCTION")
DEBUG = bool(os.getenv("DEBUG"))
# DEBUG = True

PDF_IMAGE_PLACEHOLDER = bool(os.getenv("PDF_IMAGE_PLACEHOLDER"))

ALLOWED_HOSTS = ['.construx.io']
ALLOWED_HOSTS += ['construx.local', '.construx.local', 'localhost']

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Application definition

AUTH_USER_MODEL = 'users.User'
TENANT_MODEL = 'clients.Client'
TENANT_DOMAIN_MODEL = 'clients.Domain'


ALL_AUTH_BACKEND = 'allauth.account.auth_backends.AuthenticationBackend'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    ALL_AUTH_BACKEND,
)

SHARED_APPS = [
    'django_tenants',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.forms',
    'allauth',
    'allauth.account',
    'clients',
    'users',
    'address',
]

TENANT_APPS = [
    'allauth',
    'allauth.account',
    'users',
    'groups',
    'profiles',
    'address',
    'config',
    'user_notifications',
    'calendars',
    'schedule',
    'works',
    'payments',
]

INSTALLED_APPS = [
    'django_tenants',
    'ninja_extra',
    'clients',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.forms',
    'allauth',
    'allauth.account',
    'crispy_forms',
    "crispy_bootstrap5",
    'notifications',
    'config',
    'users',
    'groups',
    'profiles',
    'address',
    'misc',
    'user_notifications',
    'calendars',
    'schedule',
    'works',
    'payments',
    # 'construx.setup.SetupConfig'
]

MIDDLEWARE = [
    'django_tenants.middleware.TenantMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'clients.middleware.ClientTenantMiddleware',
    'users.middleware.ImpersonateMiddleware',
    'config.middleware.ConfigMiddleware',
]

ROOT_URLCONF = 'construx.urls'
PUBLIC_SCHEMA_URLCONF = 'construx.urls_public'

SITE_ID = 1

# allauth configurations
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional' if DEBUG else 'mandatory'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

NOTIFICATIONS_NOTIFICATION_MODEL = 'user_notifications.Notification'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), join(APP_BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'construx.context_processors.general_info',
                'config.context_processors.subscription_mode',
                'construx.context_processors.branding',
            ],
        },
    },
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'construx.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        # TODO: load from .env
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': os.getenv("DATABASE_IP") or "localhost",
        'PORT': 5432,
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# i18n files folder
LOCALE_PATHS = (BASE_DIR / 'locales/',)

# Base url to serve media files
MEDIA_URL = '/media/'
SITE_NAME = 'Construx'
SITE_DOMAIN = os.getenv('SITE_DOMAIN')
SITE_URL = f'https://{SITE_DOMAIN}'

# Share cookie on domain
SESSION_COOKIE_DOMAIN = f'.{SITE_DOMAIN}'

# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

X_FRAME_OPTIONS = 'SAMEORIGIN'

# SMTP CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'mailhog')
EMAIL_PORT = os.getenv('EMAIL_PORT', '1025')
EMAIL_USE_TLS = bool(os.getenv('EMAIL_USE_TLS'))
EMAIL_ADDRESS = 'dev@construx.io'
EMAIL_HOST_USER = EMAIL_ADDRESS
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = EMAIL_ADDRESS
SERVER_EMAIL = EMAIL_ADDRESS
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# General
SUPPORT_URL = 'https://construx.io/support'

# S3
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_PRIVATE_MEDIA_LOCATION = '%s'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'sa-east-1'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'construx.storage.TenantS3Storage'

if not AWS_ACCESS_KEY_ID:
    DEFAULT_FILE_STORAGE = 'django_tenants.files.storage.TenantFileSystemStorage'

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

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
	},
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'console_debug_false': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
        },
        'django_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/construx/error.log',
        },
        'crawler_log': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/construx/crawler.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'console_debug_false', 'django_errors'],
            'level': 'INFO',
        },
        'document.views.render': {
            'handlers': ['console', 'console_debug_false'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'crawler.crawler': {
            'handlers': ['console', 'console_debug_false', 'crawler_log'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

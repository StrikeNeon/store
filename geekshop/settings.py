"""
Django settings for STORE project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import json
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADMINS = [("Anon", "SjasFaceMD@Gmail.com")]
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

try:
    with open('geekshop/keys.json', 'r') as f:
        DEBUG = True
        secret_keys = json.load(f)

        SECRET_KEY = secret_keys['SECRET_KEY']

        SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = secret_keys['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
        SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = secret_keys['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
        SOCIAL_AUTH_VK_OAUTH2_KEY = secret_keys['SOCIAL_AUTH_VK_OAUTH2_KEY']
        SOCIAL_AUTH_VK_OAUTH2_SECRET = secret_keys['SOCIAL_AUTH_VK_OAUTH2_SECRET']

        EMAIL_ADDRESS = secret_keys['EMAIL_ADDRESS']
        EMAIL_PASSWORD = secret_keys['EMAIL_PASSWORD']

        DB_NAME = secret_keys['DB_NAME']
        DB_USERNAME = secret_keys['DB_USERNAME']
        DB_PASSWORD = secret_keys['DB_PASSWORD']
        DB_HOST = secret_keys['DB_HOST']
        DB_PORT = secret_keys['DB_PORT']

        AWS_ACCESS_KEY_ID = secret_keys['S3_KEY']
        AWS_SECRET_ACCESS_KEY = secret_keys['S3_SECRET']
        AWS_STORAGE_BUCKET_NAME = secret_keys['S3_BUCKET']
        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

        REDIS_LOCATION = secret_keys['REDIS_URL']


except FileNotFoundError:

    #  TODO figure out why the server fails with debug set to false
    DEBUG = True

    SECRET_KEY = os.environ['SECRET_KEY']

    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
    SOCIAL_AUTH_VK_OAUTH2_KEY = os.environ['SOCIAL_AUTH_VK_OAUTH2_KEY']
    SOCIAL_AUTH_VK_OAUTH2_SECRET = os.environ['SOCIAL_AUTH_VK_OAUTH2_SECRET']

    EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
    EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

    DB_NAME = os.environ['DB_NAME']
    DB_USERNAME = os.environ['DB_USERNAME']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ['DB_PORT']

    AWS_ACCESS_KEY_ID = os.environ['S3_KEY']
    AWS_SECRET_ACCESS_KEY = os.environ['S3_SECRET']
    AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET']
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    REDIS_LOCATION = os.environ['REDIS_URL']


ALLOWED_HOSTS = ["*"]

DOMAINS = "https://test-store-a.herokuapp.com/"

# Application definition

if DEBUG:
    INSTALLED_APPS = [
        'mainapp.apps.mainappconfig',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'social_django',
        'storages',
        'django_extensions',
        'debug_toolbar',
        'template_profiler_panel',
        'redis_cache'

    ]
else:
    INSTALLED_APPS = [
        'mainapp.apps.mainappconfig',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'social_django',
        'storages',
        'redis_cache'
    ]


SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

CART_SESSION_ID = 'cart'

if DEBUG:
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)
    INTERNAL_IPS = ["127.0.0.1", "::1"]
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'social_django.middleware.SocialAuthExceptionMiddleware',
    ]

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'template_profiler_panel.panels.template.TemplateProfilerPanel',
    ]
else:
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'social_django.middleware.SocialAuthExceptionMiddleware',
    ]

ROOT_URLCONF = 'geekshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'geekshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USERNAME,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    },
    'local': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    "default": {
         "BACKEND": "redis_cache.RedisCache",
         "LOCATION": REDIS_LOCATION,
         "OPTIONS": {
            "CONNECTION_POOL_KWARGS": {
                "ssl_cert_reqs": None
            }
         }
    }
}

# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_VK_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']


LOGIN_URL = '/auth/login/google-oauth2/'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.create_user',
    'authapp.pipeline.save_user_profile',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AWS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

if not AWS:
    STATIC_URL = '/staticfiles/'
    MEDIA_URL = '/media/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

else:
    AWS_S3_OBJECT_PARAMETERS = {
            'CacheControl': 'max-age=86400',
    }
    AWS_DEFAULT_ACL = None
    STATIC_LOCATION = 'static-667"'
    STATICFILES_STORAGE = 'geekshop.storage_backends.StaticStorage'

    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"

    MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'geekshop.storage_backends.MediaStorage'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

if EMAIL_BACKEND == 'django.core.mail.backends.filebased.EmailBackend':
    EMAIL_FILE_PATH = "mail"  # debug "mail" - writes files instead of sending
else:  # configure host here
    EMAIL_USE_SSL = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = EMAIL_ADDRESS
    EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
    DEFAULT_FROM_EMAIL = EMAIL_ADDRESS

django_heroku.settings(locals())

import os
import uuid

gettext = lambda s: s  # noqa

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'demo.db')
    }
}

TIME_ZONE = 'UTC'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
MEDIA_URL = '/media/'

SECRET_KEY = str(uuid.uuid4())

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'demo.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'parler',
    'assessment'
)

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
            ],
        },
    },
]

USE_TZ = True
USE_I18N = True
USE_L10N = True

LANGUAGE_CODE = 'en'


LANGUAGES = [
    ('de', gettext('German')),
    ('en', gettext('English')),
    ('fr', gettext('French')),
    ('nl', gettext('Nederlands')),
]

# ------------------------------------------------------------------------------
# TRANSLATION Configuration
# ------------------------------------------------------------------------------
PARLER_DEFAULT_LANGUAGE_CODE = LANGUAGE_CODE
PARLER_LANGUAGES = {
    None: (
        {'code': 'de',},
        {'code': 'en',},
        {'code': 'fr',},
        {'code': 'nl',},
    ),
    'default': {
        'fallbacks': [LANGUAGE_CODE],
        'hide_untranslated': False,
    }
}

CORS_ORIGIN_ALLOW_ALL = DEBUG


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

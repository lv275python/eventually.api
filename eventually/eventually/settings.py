"""
Django settings for eventually project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p40lad8jx!=byfzjrgi40(is0lz2pzn9l+zg0(993bvj425*r$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

APPEND_SLASH = False
# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'customprofile',
    'event',
    'task',
    'team',
    'topic',
    'vote',
    'comment',
    'authentication',
    'literature',
    'home',
    'assignment',
    'item',
    'curriculum',
    'amazons3',
]

AUTH_USER_MODEL = 'authentication.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middlewares.loginrequired.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'eventually.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'eventually.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# AmazonS3
AWS_S3_ACCESS_KEY_ID = 'AWS_S3_ACCESS_KEY_ID'
AWS_S3_SECRET_ACCESS_KEY = 'AWS_S3_SECRET_ACCESS_KEY'
AWS_STORAGE_BUCKET_NAME = 'AWS_STORAGE_BUCKET_NAME'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'travis_db',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/'),]

# Required settings for sending email.

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'EMAIL_HOST_USER@gmail.com'
EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'DEFAULT_FROM_EMAIL'

# JWT Token required settings.

JWT_TOKEN_KEY = 'any secret word'
JWT_ALGORITHM = 'HS384'

FRONT_HOST = 'localhost:8000'

# Logger required settings.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': os.path.join('/var/log/', 'eventually.log'),
        },
    },
    'loggers': {
        'eventually': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(pathname)s line: %(lineno)d '
                      'message: %(message)s',
            'datefmt': '%d/%m/%Y %I:%M:%S'
        },
    },
}

SESSION_COOKIE_HTTPONLY = False

try:
    from .local_settings import *
except ImportError:
    pass

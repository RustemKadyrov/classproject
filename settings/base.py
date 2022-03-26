import os
import sys
from pathlib import Path
from .import get_env_variable
# from settings.conf import 


AUTH_USER_MODEL = 'auths.CustomUser'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'apps'))


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


ROOT_URLCONF = 'urls.urls'


SECRET_KEY = get_env_variable('SECRET_KEY') 
DEBUG = True


ALLOWED_HOSTS = ['*']
WSGI_APPLICATION = 'settings.wsgi.application'

DJANGO_AND_THIRD_PARTY_APPS = [
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
]


PROJECT_APPS = [
    'app1.apps.App1Config',
    'abstract.apps.AbstractConfig',
    'auths.apps.AuthsConfig',
]


INSTALLED_APPS = DJANGO_AND_THIRD_PARTY_APPS + PROJECT_APPS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]


INTERNAL_IPS = [
    '127.0.0.1',
]


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


# Custom constants
#
# ADMIN_SITE_URL = 'custom_admin/'


LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# STATIC_URL = '/static/'
ADMIN_SITE_URL = '12345'
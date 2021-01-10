from pathlib import Path
import os
import django_heroku
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o23cgzqp0=^d!7(!j#y$f=-$^or*=je4y)w-0y(__egg(lht)#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'guru',
    'sekolah',
    'siswa',

    'widget_tweaks',
    'solo',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'REI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'rei_tags': 'REI.templatetags.rei_tags'
            },
        },
    },
]

WSGI_APPLICATION = 'REI.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
from pymongo.mongo_client import MongoClient
MongoClient.HOST = 'mongodb://admin-munawar:L1GvzLE7C8VuCsUA@rei-database-shard-00-00.94yhc.mongodb.net:27017,rei-database-shard-00-01.94yhc.mongodb.net:27017,rei-database-shard-00-02.94yhc.mongodb.net:27017/REIMongo?ssl=true&replicaSet=atlas-770ftc-shard-0&authSource=admin&retryWrites=true&w=majority'
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'REIMongo',
        "CLIENT": {
            "host": 'mongodb://admin-munawar:L1GvzLE7C8VuCsUA@rei-database-shard-00-00.94yhc.mongodb.net:27017,rei-database-shard-00-01.94yhc.mongodb.net:27017,rei-database-shard-00-02.94yhc.mongodb.net:27017/REIMongo?ssl=true&replicaSet=atlas-770ftc-shard-0&authSource=admin&retryWrites=true&w=majority',
            "username": 'admin-munawar',
            "password": 'L1GvzLE7C8VuCsUA',
            "authMechanism": "SCRAM-SHA-1",
        },
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_DIRS = [
    BASE_DIR/'static/',
]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/'media/'

# Authentication
AUTH_USER_MODEL = 'guru.Guru'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# Stuff
DATE_FORMAT = '%d-%m-%y'

django_heroku.settings(locals())
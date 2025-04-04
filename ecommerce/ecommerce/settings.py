"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
# the timedelta is used to manipule the time , ex : delta = timedelta(hours=5, minutes=30)  # 5 heures et 30 minutes
from datetime import timedelta
import os
from decouple import config
from corsheaders.defaults import default_headers

# secure data 

FILE_PATH = config("FILE_PATH")
ADMIN = config("ADMIN")
DB_PASSWORD = config("DB_PASSWORD")
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ecomApp',
    'rest_framework',
    "corsheaders",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'ecommerce.urls'

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

WSGI_APPLICATION = 'ecommerce.wsgi.application'
SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
# This settings is for Amazon RDS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fashionista',
        'USER': 'postgres',
        'PASSWORD':DB_PASSWORD,
        'HOST': 'fashionista.cj2m2o28ou96.eu-north-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}
DATABASES['default']['CONN_MAX_AGE'] = 600
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
REST_FRAMEWORK ={
    "DEFAULT_AUTHENTICATION_CLASSES":[
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    "DEFAULT_PERMISSION_CLASSES":[
        'rest_framework.permissions.IsAuthenticated',
    ]
}
CORS_ALLOW_HEADERS = list(default_headers) + [
    "X-Google-Access-Token",
]
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME' : timedelta(days=3),
}
# Allow requests from specified server only 
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # React development server
    "http://my-fashionista.s3-website.eu-north-1.amazonaws.com" # S3 endpoint
]
CORS_ALLOW_ALL_ORIGIN = True
CROS_ALLOWS_CREDENTIALS = True
# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/images/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
MEDIA_ROOT = 'static/images'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_RIDERECT_URL = '/callback/'
SOCIALACCOUNT_PROVIDERS = {
    'google':{
        'SCOPE':['email','profile'],
        'AUTH_PARAMS':{'access_type':'online'},
        'OAUTH_PKCE_ENABLED':True,
        'FETCH_USERINFO':True
    }
}
SOCIALACCOUNT_STORE_TOKENS = True
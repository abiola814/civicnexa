"""
Django settings for Civicnexa project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z4)e-$sp41$404v$mr!)81y^-qswdx3yz)=*(2uy1ajakaafwf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'profiling',
    'payment',
    'adminpanel',
    'rest_framework',
    'djoser',
    'uritemplate',
    'corsheaders',
    'drf_yasg',
]


DJOSER = {
            'SEND_ACTIVATION_EMAIL': True,
            'USER_CREATE_PASSWORD_RETYPE': True,
            'ACTIVATION_URL': 'profiling/activate/{uid}/{token}/',
            'EMAIL':{
                'activation': 'djoser.email.ActivationEmail',
            },
            'SEND_CONFIRMATION_EMAIL': True,
            'SERIALIZER': {
                # 'user_create': 'userprofile.serializer.UserCreateSerializer',
                           'activation': 'djoser.serializers.ActivationSerializer',
                           }
          }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Civicnexa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
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

WSGI_APPLICATION = 'Civicnexa.wsgi.application'

# CORS Development settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "https://user-profilling.vercel.app",
    "http://localhost:8080",
    "http://localhost:80",
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1"
]

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES={
    "default":dj_database_url.parse("postgres://easypay:OSzd8CXJ0XDCCcP4kBVpyNIdQMlIvg2Y@dpg-cljivdtae00c7386m4o0-a.oregon-postgres.render.com/easypay_p7zu")
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL ='media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY =os.getenv('PAYSTACK_PUBLIC_KEY')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'yakubayatoo@gmail.com'
EMAIL_HOST_PASSWORD = 'xRStGXdAFOhnU94z'
DEFAULT_FROM_EMAIL = 'no-reply@civicnexa.com'


SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('','JWT', 'Bearer',),
   "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
   "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}
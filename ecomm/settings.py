"""
Django settings for ecomm project.

Generated by 'django-admin startproject' using Django 4.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import dj_database_url
from django.templatetags.static import static
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# check if DEBUG is set in env as False or true DEBUG = True in env
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = []

# CSRF_TRUSTED_ORIGINS = ['']


# Application definition

INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'compressor',
    'crispy_forms',
    'crispy_tailwind',
    'whitenoise.runserver_nostatic',
    'imagekit',


    # local apps
    # 'core',
    'user',
    'store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'core.middleware.SeparateSessionMiddleware',  # Separate session middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecomm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # custom context processor
                'store.context_processors.cart_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecomm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# compressor settings
COMPRESS_ROOT = STATIC_ROOT

COMPRESS_ENABLED = True

# COMPRESS_STORAGE = STATICFILES_DIRS

# COMPRESS_OFFLINE_MANIFEST_STORAGE = STATICFILES_DIRS

# COMPRESS_URL = STATIC_URL


# STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)


MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Whitenoise forever cache settings
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.your-email-provider.com'  # e.g., smtp.gmail.com
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your@email.com'
# EMAIL_HOST_PASSWORD = 'your-email-password'
# DEFAULT_FROM_EMAIL = 'your@email.com'
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'default-contact@example.com')
  # Where contact form emails should go

# custom user settings
AUTH_USER_MODEL = 'user.User'

# Django-unfold settings
# UNFOLD = {
#     "STYLES": [
#         lambda request: static("css/style.css"),
#     ],
#     "SCRIPTS": [
#         lambda request: static("js/script.js"),
#     ],
# }

# Paystack api settings
PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY')
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')

# # crispy_tailwind settings
CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'

CRISPY_TEMPLATE_PACK = 'tailwind'

# dj_database_url settings for db
# This block of code is used to configure the database settings based on the
# environment the application is running in. If the environment is set to
# 'production', it will read the database configuration from the
# DATABASE_URL environment variable.
#
# The DATABASES dictionary is updated with the configuration from the
# DATABASE_URL environment variable. The conn_max_age parameter is set to 1800
# seconds (30 minutes) to specify the maximum time a connection should persist.

# Get the environment from the environment variable. If the variable is not set,
# default to 'development'.
Environment = os.getenv('ENVIRONMENT', 'production')

# If the environment is set to 'production', update the database configuration.
if Environment == 'development':
    # Read the database configuration from the DATABASE_URL environment variable.
    # The conn_max_age parameter specifies the maximum time a connection should
    # persist.
    db_from_env = dj_database_url.config(conn_max_age=1800)

    # Update the default database configuration with the configuration from the
    # DATABASE_URL environment variable.
    DATABASES['default'].update(db_from_env)

# LOGINURL SETTINGS
LOGIN_URL = 'user/login/'


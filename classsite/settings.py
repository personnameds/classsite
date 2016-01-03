"""
Django settings for classsite project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
SECRET_DIRECTORY=os.path.join(BASE_DIR,'classsite')+'/SECRET_KEY'
# SECURITY WARNING: keep the secret key used in production secret!
with open(SECRET_DIRECTORY) as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS=['.mrsanyal.com','.qvic.ca']

ADMINS = (('Mr. Sanyal','mistersanyal@gmail.com'),)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'classlists',
    'schoolsetup',
    'schoolpage',
    'kalendar',
    'schedule',
    'classpage',
    'homework',
    'documents',
    'links',
    'msgs',
    'contact',
    'registration',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'classsite.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'classsite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'qvdatabase',
        'USER':'qvsite',
        'PASSWORD': '1PrtocltK7kO',
        'HOST':'localhost',
        'PORT':'3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#Static files (CSS, JavaScript, Images)
#https://docs.djangoproject.com/en/1.8/howto/static-files/
STATICFILES_DIR='/home/sudeepsanyal/webapps/qv_static/'
MEDIA_ROOT = '/home/sudeepsanyal/webapps/qv_media/'
STATIC_URL = '/static/'
MEDIA_URL='/media/'

LOGIN_REDIRECT_URL='/'
LOGIN_URL='/login/'
SCHOOL='Queen Victoria'
REGISTRATION_STATUS=True

EMAIL_HOST='smtp.webfaction.com'
EMAIL_HOST_USER='qvic'
EMAIL_HOST_PASSWORD='assandra3#'
DEFAULT_FROM_EMAIL='sudeepsanyal@sudeepsanyal.webfactional.com'
SERVER_EMAIL='sudeepsanyal@sudeepsanyal.webfactional.com'

try:
    from classsite.settings_local import *
except ImportError:
    pass
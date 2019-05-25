"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SKEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [os.environ.get('AHOST')]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'rest_framework',
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
]

ROOT_URLCONF = 'blog.urls'

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

WSGI_APPLICATION = 'blog.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blog',
		'USER': os.environ.get('userName'),
		'PASSWORD': os.environ.get('userPass'),
		'HOST': 'localhost',
		'PORT': '',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = 'static/'

# Adding a root - commenting out to get js working
STATIC_ROOT = os.path.join(BASE_DIR, "static")

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime}\t{levelname}\t{process:d}\t{thread:d}-\t{message}',
            'style': '{',
        },
        'simple': {
            'format': '{asctime}-{levelname}: {message}',
            'style': '{',
        },
    },
	'handlers': {
		'file': {
            'level': 'DEBUG',
			'class': 'logging.FileHandler',
            'filename': '/var/log/django/debug.log',
		},
        'views-debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/debug/views.log',
            'formatter': 'verbose',
        },
        'views-info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/views.log',
            'formatter': 'simple',
        },
        'rest-debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/debug/rest.log',
            'formatter': 'verbose',
        },
        'rest-info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/rest.log',
            'formatter': 'simple',
        },
        'models-debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/debug/models.log',
            'formatter': 'verbose',
        },
	},
	'loggers': {
		'django': {
			'handlers': ['file'],
			'level': 'DEBUG',
            'propagate': True,
		},
        # Need to update this to blog.views
        'viewer': {
            'handlers': ['views-debug','views-info'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'blog.rest': {
            'handlers': ['rest-debug','rest-info'],
            'level': 'DEBUG',
            'propogate': True,
        },
        'blog.models': {
            'handlers': ['models-debug'],
            'level': 'DEBUG',
            'propogate': True,
        },
	},
}

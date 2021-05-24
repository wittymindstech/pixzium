
import os
from pathlib import Path
from dotenv import dotenv_values
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
config = dotenv_values()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l)ll(*5)=y!gof=b#!ejiawcv1@&j_out4!uqtzql5%pxpygq8'
# SECRET_KEY = 'fsfs@4%mskd%s9sec1qf1$v*ix1_6lo-1iyapjahausdh3n2a3M'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Django Allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin',

    # Django Helping Hands
    'django_social_share',
    'taggit',
    'storages',
    'crispy_forms',
    'django_truncate',
    # App
    'wtgallery',

]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
            ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'linkedin': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}


ROOT_URLCONF = 'pixzium.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'pixzium.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config['DB_NAME'],  # Your AWS DB name
        'USER': config['DB_USERNAME'],  # Your AWS Username
        'PASSWORD': config['DB_PASSWORD'],  # Your AWS Password
        'HOST': 'pixziummain.cssgwjlhiewv.ap-south-1.rds.amazonaws.com',  # Your AWS Hostname
        'PORT': '5432',
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

USE_L10N = True

USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

EMAIL_HOST_USER = config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Login Settings

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# AWS Settings

AWS_LOCATION = 'static'
AWS_ACCESS_KEY_ID = config['AWS_ACCESS_KEY']  # Your AWS Access Key ID
AWS_SECRET_ACCESS_KEY = config['AWS_SECRET_KEY']  # Your AWS Secret Access Key
AWS_STORAGE_BUCKET_NAME = config['AWS_BUCKET_NAME']  # Your AWS Bucket name

AWS_S3_REGION_NAME = 'ap-south-1'  # AWS s3 Bucket region name
AWS_S3_SIGNATURE_VERSION = 's3v4'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_CLOUDFRONT_DOMAIN = 'd3gxnqjvuiz5a8.cloudfront.net'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
DEFAULT_FILE_STORAGE = 'pixzium.storage_backends.MediaStorage'
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


STATIC_URL = 'https://%s/%s/' % (AWS_S3_CLOUDFRONT_DOMAIN, AWS_LOCATION)
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
AWS_DEFAULT_ACL = None



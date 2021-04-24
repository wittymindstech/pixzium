
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l)ll(*5)=y!gof=b#!ejiawcv1@&j_out4!uqtzql5%pxpygq8'

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
    
    'wtgallery',
    'taggit',
    'storages',
    'crispy_forms',
    'django_truncate',
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'wtgallerydb',  # Your AWS DB name
#         'USER': 'wtgalleryadmin',  # Your AWS Username
#         'PASSWORD': 'redhat123',  # Your AWS Password
#         'HOST': 'wtgallerymain.cssgwjlhiewv.ap-south-1.rds.amazonaws.com',  # Your AWS Hostname
#         'PORT': '5432',
#     }
# }


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

# AWS_LOCATION = 'static'
# AWS_ACCESS_KEY_ID = ''  # Your AWS Access Key ID
# AWS_SECRET_ACCESS_KEY = ''  # Your AWS Secret Access Key
# AWS_STORAGE_BUCKET_NAME = 'mainwtgallery'  # Your AWS Bucket name
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# DEFAULT_FILE_STORAGE = 'wtGallery.storage_backends.MediaStorage'
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# )
# AWS_DEFAULT_ACL = None


# AWS_ACCESS_KEY_ID = "AKIA2QMUNTD5LYJEECAV"
# AWS_SECRET_ACCESS_KEY = "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"
# AWS_STORAGE_BUCKET_NAME = "mainwtgallery"
#
# AWS_S3_CLOUDFRONT_DOMAIN_MEDIA = "d2g0zd6flkd76r.cloudfront.net"
# AWS_S3_CLOUDFRONT_DOMAIN_STATIC = "d2usq1dexjp4d9.cloudfront.net"
# AWS_S3_OBJECT_PARAMETERS = {
#      'CacheControl': 'max-age=86400',
# }
#
# STATICFILES_LOCATION = 'static'
# STATIC_ROOT = '/%s/' % STATICFILES_LOCATION
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CLOUDFRONT_DOMAIN_STATIC, STATICFILES_LOCATION)
# STATICFILES_STORAGE = 'wtGallery.storage_backends.StaticStorage'
#
# MEDIAFILES_LOCATION = 'media'
# MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CLOUDFRONT_DOMAIN_MEDIA, MEDIAFILES_LOCATION)
# DEFAULT_FILE_STORAGE = 'wtGallery.storage_backends.MediaStorage'
#
# ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
# STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder',)
# AWS_DEFAULT_ACL = None

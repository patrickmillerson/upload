import os
from pathlib import Path

import environ

# Initialize environment variables
env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

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
    'storages',
    'app'
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

ROOT_URLCONF = 'upload.urls'

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

WSGI_APPLICATION = 'upload.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

# MEDIA_URL is the public URL for accessing media files
# MEDIA_URL = '/media/'
if os.environ.get('DJANGO_ENV') == 'development':
    # Use local file serving in development
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    MEDIA_URL = 'https://{}/'.format(os.environ.get("B2_BUCKET_NAME"))

# MEDIA_ROOT is the absolute path to the directory where uploaded files will be stored
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Default storage configuration for Backblaze B2
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage"
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
    }
}

# Backblaze B2 credentials
# B2_BUCKET_NAME = os.environ.get("B2_BUCKET_NAME")
# B2_ACCOUNT_ID = os.environ.get("B2_ACCOUNT_ID")
# B2_APPLICATION_KEY = os.environ.get("B2_APPLICATION_KEY")


AWS_ACCESS_KEY_ID = os.environ.get("B2_ACCOUNT_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("B2_APPLICATION_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("B2_BUCKET_NAME")

# Backblaze S3 Endpoint (Replace with your actual region)
AWS_S3_ENDPOINT_URL = "https://s3.us-west-002.backblazeb2.com"  

AWS_S3_ADDRESSING_STYLE = "path"
AWS_QUERYSTRING_AUTH = False  # Public access (True = Signed URLs)

B2_APP_KEY_ID = os.environ.get('B2_ACCOUNT_ID')
B2_APP_KEY = os.environ.get('B2_APPLICATION_KEY')
B2_BUCKET_NAME = os.environ.get('B2_BUCKET_NAME')
B2_ACCOUNT_ID = os.environ.get('B2_ACCOUNT_ID')
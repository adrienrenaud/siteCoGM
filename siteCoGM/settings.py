"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pallcvt&qv%)xfnfwn4&+q2i!7l_6w(^x*8vuh*nb!33e6l&g^'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['.arenaud.kd.io']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'analytical',
    'storages',
    'south',
    'siteCoGM.apps.userdata',
    'django_cleanup', # should go after your apps
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)



STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


CLICKY_SITE_ID = '100698442'

GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-46616768-1'
GOOGLE_ANALYTICS_INTERNAL_IPS = [os.environ.get('MY_IP')]
ANALYTICAL_INTERNAL_IPS = [os.environ.get('MY_IP')]





ROOT_URLCONF = 'siteCoGM.urls'

WSGI_APPLICATION = 'siteCoGM.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.media",
    )



TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'siteCoGM/templates')
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True





# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
# STATIC_URL = '/static/'

# Additional locations of static files
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'siteCoGM/static'),
#     # Put strings here, like "/home/html/static" or "C:/www/django/static".
#     # Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths.
# )




# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']



# MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 
# STATIC_ROOT = 'static'

MEDIA_ROOT = 'media' 
STATIC_ROOT = 'static'


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'siteCoGM/static'),
)



AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# AWS_STORAGE_BUCKET_NAME = 'adrienrenauds3bucket'
AWS_STORAGE_BUCKET_NAME = 'adrienrenauds3bucketdev'

DEFAULT_FILE_STORAGE = 'siteCoGM.s3utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'siteCoGM.s3utils.StaticRootS3BotoStorage'     


S3_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
MEDIA_URL = S3_URL + 'media/'
STATIC_URL = S3_URL + 'static/'

AWS_REDUCED_REDUNDANCY = False # We enable this server-wide on our staging server's S3 buckets
AWS_PRELOAD_METADATA = True # You want this to be on!


## redirection url for the login_requiered decorator 
LOGIN_URL = '/CoGM/login/'



EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
EMAIL_HOST= 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')



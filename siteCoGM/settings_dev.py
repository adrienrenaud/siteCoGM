from siteCoGM.settings import *
import os 

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = True



DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'    


MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'mydb',
        # 'USER': 'foo',
        # 'PASSWORD': 'bar',
        'NAME': 'cogm_db',
        'USER': 'arenaud',
        'PASSWORD': 'marignan',
        'HOST':'localhost',
        'PORT':'5432'
    }
}

from siteCoGM.settings import *


DEBUG = True
TEMPLATE_DEBUG = True



DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'    


MEDIA_URL = '/media/'
STATIC_URL = '/static/'

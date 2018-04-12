from terraform_manager.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'terraform_manager',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

BROKER_URL = 'redis://:6379/0'
CELERY_RESULT_BACKEND = 'redis://:6379/0'

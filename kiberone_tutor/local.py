from kiberone_tutor.base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tutor_kiberone',
        'USER': 'postgres',
        'PASSWORD': 'HorizonEvent',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/home/alexey/tutor-kiberone/static'
STATICFILES_DIRS = [BASE_DIR, 'fair', 'static']

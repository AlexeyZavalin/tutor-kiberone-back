from kiberone_tutor.base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_NAME', 'tutor_kiberone'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'HorizonEvent'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': '5432'
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/home/alexey/tutor-kiberone/static'
STATICFILES_DIRS = [BASE_DIR, 'fair', 'static']

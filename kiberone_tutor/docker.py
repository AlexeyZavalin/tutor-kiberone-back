from kiberone_tutor.base import *

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = int(os.environ.get("DEBUG", default=0))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432'
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/home/alexey/tutor-kiberone/static'
STATICFILES_DIRS = [BASE_DIR, 'fair', 'static']

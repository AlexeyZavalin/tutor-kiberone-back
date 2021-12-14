from kiberone_tutor.base import *

DEBUG = False

STATIC_URL = '/assets/'
STATIC_ROOT = '/home/alexey/sites/tutor-kiberone-back/assets'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('db_name'),
        'USER': os.environ.get('db_user'),
        'PASSWORD': os.environ.get('db_password'),
        'HOST': os.environ.get('db_host'),
        'PORT': os.environ.get('db_port'),
    }
}

#sentry
sentry_sdk.init(
    dsn=os.environ.get('sentry_dsn'),
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# email region

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.environ.get('email_host')
EMAIL_PORT = os.environ.get('email_port')
EMAIL_HOST_USER = os.environ.get('email_host_user')
EMAIL_HOST_PASSWORD = os.environ.get('email_host_password')
EMAIL_USE_TLS = os.environ.get('email_user_tls') == 'True'

from kiberone_tutor.base import *

DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")

STATIC_URL = '/assets/'
STATIC_ROOT = os.environ.get('STATIC_ROOT')

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

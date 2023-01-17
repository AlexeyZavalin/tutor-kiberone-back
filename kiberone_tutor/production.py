from kiberone_tutor.base import *

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

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

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = bool(int(os.environ.get('EMAIL_USE_SSL', '0')))
CSRF_COOKIE_SECURE = bool(int(os.environ.get('CSRF_COOKIE_SECURE', '1')))
SESSION_COOKIE_SECURE = bool(int(os.environ.get('SESSION_COOKIE_SECURE', '1')))

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

from .base import *


DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = '7h30jdt)hia_ns_xhwf3jxk1#wdnqff0g8)cc6%agk^vl#!y#0'
DATABASES['default']['PASSWORD'] = ''

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass

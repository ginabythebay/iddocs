import os

from django.conf import settings

from main import *

MIDDLEWARE.append('middleware.SecureOnly')
MIDDLEWARE.append('django.contrib.auth.middleware.RemoteUserMiddleware')
MIDDLEWARE.append('apache_auth.middleware.HttpAuthMiddleware')

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.RemoteUserBackend',
]

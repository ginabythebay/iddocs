import os

from django.conf import settings


settings.MIDDLEWARE.append('middleware.SecureOnly')

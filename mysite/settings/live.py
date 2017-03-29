import os

from django.conf import settings

from main import *


MIDDLEWARE.append('middleware.SecureOnly')

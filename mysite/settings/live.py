import os

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split()
STATIC_ROOT = os.environ['STATIC_ROOT']

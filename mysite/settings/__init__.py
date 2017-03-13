import os

dev = os.environ.get('DJANGO_DEV', False)

from main import *

if dev:
    from dev import *
else:
    from live import *


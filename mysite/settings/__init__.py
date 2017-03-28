import os

from main import *

if DJANGO_DEV:
    from dev import *
else:
    from live import *


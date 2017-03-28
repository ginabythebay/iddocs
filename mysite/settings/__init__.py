import os


from env import (
    DJANGO_DEV,
)


from main import *

if DJANGO_DEV:
    from dev import *
else:
    from live import *


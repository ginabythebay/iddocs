import os


from env import (
    DJANGO_DEV,
)


if DJANGO_DEV:
    from dev import *
else:
    from live import *


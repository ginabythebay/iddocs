import os


from env import (
    ALLOWED_HOSTS,
    BACKUP_ROOT,
    BUILD_DIR,
    BUILD_LINK ,
    BUILD_TMP_DIR,
    DJANGO_DEV,
    MEDIA_ROOT,
    MYSQL_DB,
    MYSQL_HOST,
    MYSQL_PWD,
    MYSQL_USER,
    PUBLISH_DIR,
    PUBLISH_LINK ,
    SECRET_KEY,
    STATIC_ROOT,
    TEST_SQLITE3,
)


from main import *

if DJANGO_DEV:
    from dev import *
else:
    from live import *


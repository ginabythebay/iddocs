
# ID Docs App

A work in progress

## Getting Started

### Set up tools

```
git clone git@github.com:ginabythebay/iddocs.git
cd iddocs
sudo pacman -S python2 python2-virtualenv python2-pip
virtualenv2 venv
. ./venv/bin/activate

pip install -r requirements.txt 

```

### Create .env file


```
cat << EOF > .env
TEST_SQLITE3="<True_or_False>"
#DJANGO_DEV="True"
ALLOWED_HOSTS=""
SECRET_KEY=$(make genkey)
BUILD_DIR="somepath"
PUBLISH_DIR="somepath"
BUILD_LINK = "some_url"
PUBLISH_LINK = "som_url"
MYSQL_USER="someuser"
MYSQL_PWD="somepwd"
MYSQL_DB="somedbname"
MYSQL_HOST="somehost"
STATIC_ROOT="somepath"
BACKUP_ROOT="somedir"
EOF
```

### Create mysql configuration file

```
cat << EOF > mysite/my.conf
[client]
default-character-set = utf8
host = yourmysqlhost
database = yourdb
user = yourdbuser
password = yourdbpwd
EOF
```

Edit the entries above

### Set up Db and start local server

```
make migrate
make createsuperuser
python manage.py loaddata locations/fixtures/states.yaml
python manage.py collectstatic
make serve
```


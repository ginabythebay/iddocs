
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
DJANGO_DEV="TRUE"
ALLOWED_HOSTS=""
SECRET_KEY=$(make genkey)
BUILD_DIR="somepath"
STATIC_ROOT="somepath"
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

## Choosing a state

Clickable maps sound nice.  Some possible solutions:

* https://newsignature.github.io/us-map/
* https://www.amcharts.com/download/ (costs money)
* http://createaclickablemap.com/ (but it depends on their server :()

## Things to solve for deployment


* add site search: https://support.google.com/customsearch/answer/4541888?hl=en
* backups.  See https://github.com/django-dbbackup/django-dbbackup and https://github.com/nathan-osman/django-archive/blob/master/docs/settings.rst
* can we turn off http? (first try redirected to .../public, which is borken)
* set up (sitemaps)[https://docs.djangoproject.com/en/1.10/ref/contrib/sitemaps/]
* Read (this)[https://www.djangorocks.com/tutorials/setting-up-your-server-to-run-django.html]
* figure out the db we will use

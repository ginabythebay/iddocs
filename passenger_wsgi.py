import sys, os

cwd = os.getcwd()

INTERP = cwd + "/venv/bin/python"
#INTERP is present twice so that the new python interpreter knows the actual executable path
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(cwd)

sys.path.insert(0,cwd+'/venv/bin')
sys.path.insert(0,cwd+'/venv/lib/python2.7/site-packages/django')
sys.path.insert(0,cwd+'/venv/lib/python2.7/site-packages')
  
import dotenv

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
 
from django.core.wsgi import get_wsgi_application

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
import django.core.management
utility = django.core.management.ManagementUtility()
command = utility.fetch_command('runserver')

command.check()

import django.conf
import django.utils

django.utils.translation.activate(django.conf.settings.LANGUAGE_CODE)

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

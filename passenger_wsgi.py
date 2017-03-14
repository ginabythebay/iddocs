import sys, os

cwd = os.getcwd()

INTERP = cwd + "/venv/bin/python"
#INTERP is present twice so that the new python interpreter knows the actual executable path
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(cwd)
sys.path.append(cwd + '/mysite')
 
sys.path.insert(0,cwd+'/venv/bin')
sys.path.insert(0,cwd+'/venv/lib/python2.7/site-packages/django')
sys.path.insert(0,cwd+'/venv/lib/python2.7/site-packages')
 
import dotenv

from django.core.wsgi import get_wsgi_application

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()

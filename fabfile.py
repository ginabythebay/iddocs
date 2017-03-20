import os
import os.path

from tempfile import mkstemp

from fabric.api import local, settings, abort, run, cd
from fabric.decorators import hosts
from fabric.utils import abort

try:
    import env
except ImportError:
    abort('''Missing env.py.
Create env.py with content like:

HOST = 'user@host'

PROD = {
  'root': '<yourfileroot>'
}

STAGING = {
  'root': '<yourfileroot>'
}

ACTIVATE = 'source ./venv/bin/activate'
''')

def virtualenv(command):
    run(env.ACTIVATE + '&&' + command)


def manage(subcommand):
    cmd = 'python manage.py ' + subcommand
    virtualenv(cmd)

@hosts(env.HOST)
def stage():
    snapshot = os.path.join(env.STAGING['root'], 'backups', 'prodsnapshot.dump')
    try:
        os.remove(snapshot)
    except OSError:
        pass

    with cd(env.PROD['root']):
        manage('dbbackup --output-path %s' % (snapshot))

    with cd(env.STAGING['root']):
        run('git pull')
        virtualenv('pip install -r requirements.txt')
        manage('flush --noinput')
        manage('migrate')
        manage('collectstatic --noinput')
        manage('dbrestore --noinput --input-path %s' % (snapshot))
        manage('build')
        run('touch tmp/restart')


@hosts(env.HOST)
def prod():
    with cd(env.PROD['root']):
        manage('dbbackup')
        run('git pull')
        virtualenv('pip install -r requirements.txt')
        manage('migrate')
        manage('collectstatic --noinput')
        manage('build')
        run('touch tmp/restart')


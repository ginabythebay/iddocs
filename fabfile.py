import os
import os.path

from tempfile import mkstemp

from fabric.api import local, settings, abort, run, cd
from fabric.decorators import hosts
from fabric.utils import abort

try:
    import fabenv
except ImportError:
    abort('''Missing fabenv.py.
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
    run(fabenv.ACTIVATE + '&&' + command)


def manage(subcommand):
    cmd = 'python manage.py ' + subcommand
    virtualenv(cmd)

@hosts(fabenv.HOST)
def get_artifact(version, name):
    run('mkdir -p ~/releases/%s' % version)
    with cd('~/releases/%s' % version):
        run('rm -f %s' % name)
        run('wget "https://github.com/ginabythebay/iddocs/releases/download/%s/%s"' % (version, name))


@hosts(fabenv.HOST)
def fetch(version):
    get_artifact(version, 'source.tar.bz2')
    get_artifact(version, 'source.sha512')
    with cd('~/releases/%s' % version):
        run('shasum -a 512 -c source.sha512')


def extract(version):
    """Extracts the versioned file into the current directory.  Assumes
       fetch has already been run."""
    run('tar xfj ~/releases/%s/source.tar.bz2' % version)


@hosts(fabenv.HOST)
def stage(version):
    fetch(version)

    dbsnapshot = os.path.join(fabenv.STAGING['root'], 'backups', 'prodsnapshot.dump')
    try:
        os.remove(dbsnapshot)
    except OSError:
        pass

    mediasnapshot = os.path.join(fabenv.STAGING['root'], 'backups', 'prodsnapshot.media.tar')
    try:
        os.remove(mediasnapshot)
    except OSError:
        pass

    with cd(fabenv.PROD['root']):
        manage('dbbackup --output-path %s' % (dbsnapshot))
        manage('mediabackup --output-path %s' % (mediasnapshot))

    with cd(fabenv.STAGING['root']):
        extract(version)
        virtualenv('pip install -r requirements.txt')
        manage('flush --noinput')
        manage('collectstatic --noinput')

        # We do this to ensure that any new tables are cleared out.
        # Otherwise when we restore from prod below, we will end up
        # not knowing migration status for tables that are sitting
        # around from staging before the restore.
        db = fabenv.STAGING['db']
        clearcmd = 'echo "drop database %s; create database %s;" | python manage.py dbshell' % (db, db)
        virtualenv(clearcmd)
        manage('dbrestore --noinput --input-path %s' % (dbsnapshot))
        run('rm -rf public/media/*')
        manage('mediarestore --noinput --input-path %s' % (mediasnapshot))
        manage('migrate')
        manage('test')
        manage('build')
        manage('rewrite_htpasswd')
        run('pkill python || true')
        run('touch tmp/restart')


@hosts(fabenv.HOST)
def prod(version):
    with cd(fabenv.PROD['root']):
        manage('dbbackup')
        manage('mediabackup')
        extract(version)
        virtualenv('pip install -r requirements.txt')
        manage('migrate')
        manage('collectstatic --noinput')
        manage('test')
        manage('build')
        run('pkill python || true')
        run('touch tmp/restart')


from django.core.management.base import BaseCommand, CommandError

from apache_auth.middleware import rewrite_htpasswd

class Command(BaseCommand):
    help = 'Rewrites the htpasswd file'

    def handle(self, *args, **options):
        written_users = rewrite_htpasswd()
        verbosity = options['verbosity']
        if verbosity >= 2:
            self.stdout.write('Wrote the following users:')
            for u in written_users:
                self.stdout.write('   %s' % u)
        if verbosity >= 1:
            self.stdout.write(self.style.SUCCESS(
                '%s users written' % len(written_users)))

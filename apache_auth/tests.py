import os.path
import shutil
import subprocess
import tempfile
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

import htpasswd

from django.conf import settings
from django.test import TestCase

from test_helpers import BaseTestCase
from test_helpers import create_staff


def _recrypt(alg, salt, pwd):
    return subprocess.check_output([
        'openssl',
        'passwd',
        '-%s' % alg,
        '-salt', salt,
        pwd])


class HttpPasswdTests(BaseTestCase):

    def _verify(self, expected_pairs):
        expected = OrderedDict()
        for user, password in expected_pairs:
            expected[user] = password
        with htpasswd.Basic(settings.HTPASSWD_PATH) as found:
            self.assertEqual(expected.keys(), found.new_users.keys())
            for item in expected.items():
                user = item[0]
                pwd = item[1]
                hash = found.new_users[user]
                _, alg, salt, value = hash.split('$', 3)
                self.assertEqual(hash, _recrypt(alg, salt, pwd))

    def test_scenario(self):

        dir = tempfile.mkdtemp()
        settings.HTPASSWD_PATH = os.path.join(dir, 'htpasswd')
        try:
            create_staff('foo', 'foo')
            self._verify([('foo', 'foo')])

            bar = create_staff('bar', 'bar')
            self._verify([('foo', 'foo'), ('bar', 'bar')])

            baz = create_staff('baz', 'baz')
            self._verify([('foo', 'foo'), ('bar', 'bar'), ('baz', 'baz')])

            bar.delete()
            self._verify([('foo', 'foo'), ('baz', 'baz')])

            baz.set_password('not_baz')
            baz.save()

            self._verify([('foo', 'foo'), ('baz', 'not_baz')])
        finally:
            shutil.rmtree(dir, ignore_errors=True)


import base64

from django.contrib.auth.models import Permission
from django.contrib.auth.models import User

from django.test import TestCase

from django.test.client import MULTIPART_CONTENT

# Run our tests against something like the live environment
import mysite.settings.live


def create_staff(username, password, **kwargs):
    user = User.objects.create_user(username=username, password=password)
    user.is_staff = True

    if 'perms' in kwargs:
        perms = kwargs['perms']
        if isinstance(perms, (str, unicode)):
            perms = (perms,)

        for p in perms:
            user.user_permissions.add(Permission.objects.get(codename=p))
    user.save()
    return user


class BaseTestCase(TestCase):
    """
    Like TestCase, but adds secure_get and secure_post which send requests
    that, for testing purposes, appear to be secure.

    Adapted from http://codeinthehole.com/tips/testing-https-handling-in-django/
    """

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.credentials = None
        self.username = None

    def _environ(self):
        cred = None
        if hasattr(self, 'credentials') and self.credentials:
            cred = self.credentials
        username = None
        if hasattr(self, 'username'):
            username = self.username
        return {
            'wsgi.url_scheme': 'https',
            'HTTP_AUTHORIZATION': cred,
            'REMOTE_USER': username,
        }

    def login(self, username, password):
        self.client.login(username=username, password=password)
        self.username = username
        self.credentials = base64.b64encode(':'.join([username, password]))

    def secure_get(self, path, data=None, follow=False, secure=False):
        return self.client.get(path, data, follow, secure,
                               **self._environ())

    def secure_post(self, path, data=None, content_type=MULTIPART_CONTENT,
                    follow=False, secure=False):
        return self.client.post(path, data, content_type, follow, secure,
                                **self._environ())

import base64
import logging

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

import htpasswd

from .models import EncryptedPwd


logger = logging.getLogger('django.security')


def _rewrite_htpasswd():
    users = User.objects.all()
    with open(settings.HTPASSWD_PATH, 'a'):
        pass
    with htpasswd.Basic(settings.HTPASSWD_PATH, 'md5') as userdb:
        userdb.new_users.clear()
        for u in users:
            if hasattr(u, 'encryptedpwd'):
                enc = u.encryptedpwd
                userdb.new_users[u.username] = enc.pwd


def _hash(pwd):
    basic = htpasswd.Basic(None, 'md5')
    basic.add('someuser', pwd)
    return basic.new_users['someuser']


class PasswordChangeMonitor(object):
    def password_changed(self, raw_pwd, user=None):
        if user == None:
            logger.info("Ignore password change with no user specified")
            return

        hash = _hash(raw_pwd)

        if hasattr(user, 'encryptedpwd'):
            entry = user.encryptedpwd
            entry.pwd = hash
            entry.save()
        else:
            entry = EncryptedPwd.objects.create(user=user, pwd=hash)

        _rewrite_htpasswd()

    def validate(self, password, user=None):
        pass

    def get_help_text(self):
        return ''


@receiver(post_delete, sender=User)
def user_deleted(sender, instance, **kwargs):
    _rewrite_htpasswd()


class HttpAuthMiddleware(object):
    """
    Middleware that verifies the HTTP_AUTHORIZATION header matches a
    username/password in the database.

    Can be used to double-check that we aren't being accessed, for
    instance, because an attacker guessed the first 8 characters of a
    users password (which is also htpasswd md5 checks apparently).
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        header = request.META.get('HTTP_AUTHORIZATION', '')
        if not credentials:
            if request.user.is_authenticated:
                auth.logout(request)
            logger.error('Request with no HTTP_AUTHORIZATION header', extra={'request': request})
            return self.get_response(request)

        tokens = header.split(' ', 1)
        if len(tokens) != 2:
            if request.user.is_authenticated:
                auth.logout(request)
            logger.error('Request with invalid HTTP_AUTHORIZATION (expected 2 tokens)', extra={'request': request})
            return self.get_response(request)

        basic, credential = tokens
        if basic.lower() != 'basic':
            if request.user.is_authenticated:
                auth.logout(request)
            logger.error('unexpected authorization type [%s] in HTTP_AUTHORIZATION' % basic, extra={'request': request})
            return self.get_response(request)

        values = base64.b64decode(credentials).split(':')
        if len(values) != 2:
            if request.user.is_authenticated:
                auth.logout(request)
            logger.error('Request with invalid HTTP_AUTHORIZATION header', extra={'request': request})
            return self.get_response(request)

        user = auth.authenticate(username=values[0], password=values[1])
        if user is None:
            if request.user.is_authenticated:
                auth.logout(request)
            logger.error('Request HTTP_AUTHORIZATION header containing invalid credentials', extra={'request': request})
            return self.get_response(request)

        return self.get_response(request)

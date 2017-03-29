from django.test import TestCase

from django.test.client import MULTIPART_CONTENT


class SecureTestCase(TestCase):
    """
    Like TestCase, but adds secure_get and secure_post which send requests 
    that, for testing purposes, appear to be secure.
    
    Adapted from http://codeinthehole.com/tips/testing-https-handling-in-django/
    """

    def secure_get(self, path, data=None, follow=False, secure=False):
        return self.client.get(path, data, follow, secure,
                               **{'wsgi.url_scheme': 'https'})

    def secure_post(self, path, data=None, content_type=MULTIPART_CONTENT,
                    follow=False, secure=False):
        return self.client.post(path, data, content_type, follow, secure,
                                **{'wsgi.url_scheme': 'https'})

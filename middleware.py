
from django.core.exceptions import SuspiciousOperation

class SecureOnly(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.is_secure():
            raise SuspiciousOperation(
                "http request received when only https requests are allowed.  "
                "This probably indicates a configuration problem with the web "
                "server between this server and the internet."
            )
        return self.get_response(request)

from django.urls import reverse

from locations.models import Location

from bcs.models import BirthCertificate
from test_helpers import SecureTestCase


def create_location(abbrev, name):
    return Location.objects.create(abbrev=abbrev, name=name)


def create_bc(location):
    text = "Pretend this is an article about %s" % location.name
    return BirthCertificate.objects.create(location=location, article=text)


class BirthCertificateListViewTests(SecureTestCase):
    def test_scenario(self):
        """
        Creates 3 locations with entries for two birth certificates
        and verifies that those 2 show up in the context.
        """
        al = create_location('al', 'Alabama')
        ak = create_location('ak', 'Alaska')
        az = create_location('az', 'Arizona')

        create_bc(ak)
        create_bc(az)

        response = self.secure_get(reverse('bcs:list'))
        self.assertQuerysetEqual(
            response.context['list'],
            ['<BirthCertificate: Alaska>', '<BirthCertificate: Arizona>']
        )

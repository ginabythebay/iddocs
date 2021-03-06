from django.urls import reverse
from mock.mock import patch

from snapshots.models import Snapshot
from test_helpers import BaseTestCase
from test_helpers import create_staff


class SnapshotsViewPermTests(BaseTestCase):

    def setUp(self):
        super(SnapshotsViewPermTests, self).setUp()
        Snapshot().save()
        create_staff('loggedinuser', 'pwd')
        create_staff('publisher', 'pwd', perms='can_publish')

    def _verify_create(self, expect):
        with patch('snapshots.views._build', autospec=True) as mock_build:
            r = self.secure_post(reverse('snapshots:create'))
            self.assertEqual(r.status_code, 302)
        self.assertEqual(mock_build.call_count, expect)

    def _verify_publish(self, expect):
        snap_query = Snapshot.objects.all()[:1]
        snap = snap_query[0]
        with patch('snapshots.views._replace', autospec=True) as mock_replace:
            r = self.secure_post(reverse('snapshots:publish'),
                                 {'snapshotid': str(snap.id)})
            self.assertEqual(r.status_code, 302)
        self.assertEqual(mock_replace.call_count, expect)

    def test_anonymous(self):
        """
        Verifies that a non-logged in user cannot see snapshot info and that
        she cannot create snapshots or publish them.
        """
        r = self.secure_get(reverse('snapshots:index'))
        self.assertEqual(r.status_code, 302)
        self.assertIn("/login", r.url)

        self._verify_create(0)
        self._verify_publish(0)

    def test_loggedin(self):
        """
        Verifies that a logged in user can see snapshot info, but no
        form buttons and that she cannot create snapshots or publish them.
        """
        self.login('loggedinuser', 'pwd')
        r = self.secure_get(reverse('snapshots:index'))
        self.assertContains(r, "Latest snapshot")
        self.assertNotContains(r, "form")

        self._verify_create(0)
        self._verify_publish(0)

    def test_publisher(self):
        """
        Verifies that a publisher can see snapshot info, and
        form buttons and that she can create snapshots and publish them.
        """
        self.login('publisher', 'pwd')
        r = self.secure_get(reverse('snapshots:index'))
        self.assertContains(r, "Latest snapshot")
        self.assertContains(r, "form", count=4)  # 2 begin forms and 2 end forms

        self._verify_create(1)
        self._verify_publish(1)


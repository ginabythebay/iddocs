
from django.contrib.auth.models import Permission, User

from django.test import TestCase

from django.urls import reverse
from mock.mock import patch

from snapshots.models import Snapshot


def _create_staff(username, **kwargs):
    user = User.objects.create_user(username=username, password="pwd")
    user.is_staff = True

    if 'perms' in kwargs:
        perms = kwargs['perms']
        if isinstance(perms, (str, unicode)):
            perms = (perms,)

        for p in perms:
            user.user_permissions.add(Permission.objects.get(codename=p))
    user.save()
    return user


class SnapshotsViewPermTests(TestCase):

    def setUp(self):
        Snapshot().save()

        _create_staff("loggedinuser")
        _create_staff("publisher", perms="can_publish")

    def _verify_create(self, expect):
        with patch('snapshots.views._build', autospec=True) as mock_build:
            r = self.client.post(reverse('snapshots:create'))
            self.assertEqual(r.status_code, 302)
        self.assertEqual(mock_build.call_count, expect)

    def _verify_publish(self, expect):
        snap_query = Snapshot.objects.all()[:1]
        snap = snap_query[0]
        with patch('snapshots.views._replace', autospec=True) as mock_replace:
            r = self.client.post(reverse('snapshots:publish'),
                                 {'snapshotid': str(snap.id)})
            self.assertEqual(r.status_code, 302)
        self.assertEqual(mock_replace.call_count, expect)

    def test_anonymous(self):
        """
        Verifies that a non-logged in user cannot see snapshot info and that
        she cannot create snapshots or publish them.
        """
        r = self.client.get(reverse('snapshots:index'))
        self.assertEqual(r.status_code, 302)
        self.assertIn("/login", r.url)

        self._verify_create(0)
        self._verify_publish(0)

    def test_loggedin(self):
        """
        Verifies that a logged in user can see snapshot info, but no
        form buttons and that she cannot create snapshots or publish them.
        """
        self.client.login(username='loggedinuser', password='pwd')
        r = self.client.get(reverse('snapshots:index'))
        self.assertContains(r, "Latest snapshot")
        self.assertNotContains(r, "form")

        self._verify_create(0)
        self._verify_publish(0)

    def test_publisher(self):
        """
        Verifies that a publisher can see snapshot info, and
        form buttons and that she can create snapshots and publish them.
        """
        self.client.login(username='publisher', password='pwd')
        r = self.client.get(reverse('snapshots:index'))
        self.assertContains(r, "Latest snapshot")
        self.assertContains(r, "form", count=4)  # 2 begin forms and 2 end forms

        self._verify_create(1)
        self._verify_publish(1)


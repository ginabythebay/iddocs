from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from django.db import models

@python_2_unicode_compatible
class Snapshot(models.Model):
    added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        Snapshot.objects.exclude(id=self.id).delete()
        super(Snapshot, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.added)


class Publication(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    snapshot_number = models.IntegerField()
    snapshot_time = models.DateTimeField()

    @classmethod
    def create(cls, snap):
        return cls(snapshot_number=snap.id, snapshot_time=snap.added)

    def save(self, *args, **kwargs):
        Publication.objects.exclude(id=self.id).delete()
        super(Publication, self).save(*args, **kwargs)

    def __str__(self):
        return 'snapshot %s' % self.snapshot_number

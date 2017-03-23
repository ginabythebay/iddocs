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


#possible states:
#  snapshot never done
#  snapshot done, never published
#  snapshot was published, never another snapshot
#  snapshot was published, newer snapshot made
#
#  maybe we have snapshot
#    number
#    creation time
#
#  publication
#    snapshot number
#    snapshot time
#    creation time

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from locations.models import Location


@python_2_unicode_compatible
class CourtOrder(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    article = MarkdownxField()
    location = models.OneToOneField(
        Location,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def formatted_article(self):
        return markdownify(self.article)

    def __str__(self):
        return self.location.name

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from locations.models import Location


@python_2_unicode_compatible
class FederalDoc(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(primary_key=True, max_length=255)
    article = MarkdownxField()

    @property
    def formatted_article(self):
        return markdownify(self.article)

    def __str__(self):
        return self.name

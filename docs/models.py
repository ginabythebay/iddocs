from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

@python_2_unicode_compatible
class Location(models.Model):
    abbrev = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class BirthCertificate(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    article = MarkdownxField(help_text='Markdown please')
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


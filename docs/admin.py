from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from .models import BirthCertificate, Location

admin.site.register(BirthCertificate, MarkdownxModelAdmin)
admin.site.register(Location)

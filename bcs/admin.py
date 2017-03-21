from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from .models import BirthCertificate

class BirthCertificateAdmin(MarkdownxModelAdmin):
    fields = ['location', 'article']

admin.site.register(BirthCertificate, BirthCertificateAdmin)

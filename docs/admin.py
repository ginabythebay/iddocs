from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from .models import BirthCertificate

admin.site.register(BirthCertificate, MarkdownxModelAdmin)

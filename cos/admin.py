from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from .models import CourtOrder

admin.site.register(CourtOrder, MarkdownxModelAdmin)

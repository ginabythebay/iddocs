from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from .models import CourtOrder

class CourtOrderAdmin(MarkdownxModelAdmin):
    fields = ['location', 'article']

admin.site.register(CourtOrder, CourtOrderAdmin)

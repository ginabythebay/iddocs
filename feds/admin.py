from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from .models import FederalDoc

admin.site.register(FederalDoc, MarkdownxModelAdmin)

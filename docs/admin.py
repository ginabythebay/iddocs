from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from .models import BirthCertificate, Location

class LocationAdmin(admin.ModelAdmin):
    list_display = ('abbrev','name')

admin.site.register(BirthCertificate, MarkdownxModelAdmin)
admin.site.register(Location, LocationAdmin)

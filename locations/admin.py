from django.contrib import admin

from .models import Location

class LocationAdmin(admin.ModelAdmin):
    list_display = ('abbrev','name')

admin.site.register(Location, LocationAdmin)

from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from .models import BirthCertificate, CourtOrder, FederalDoc

admin.site.register(BirthCertificate, MarkdownxModelAdmin)
admin.site.register(CourtOrder, MarkdownxModelAdmin)
admin.site.register(FederalDoc, MarkdownxModelAdmin)


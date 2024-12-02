from django.contrib import admin

from ..models import PermitReplacement

class PermitReplacementAdmin(admin.ModelAdmin):
    list_display = (
        'date_signed',
        'signature',
        'certificate_status',
    )
    search_fields = ('certificate_status',)
    list_filter = ('certificate_status', 'date_signed',)

admin.site.register(PermitReplacement, PermitReplacementAdmin)
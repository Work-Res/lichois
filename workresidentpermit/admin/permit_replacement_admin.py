from django.contrib import admin
from typing import Tuple
from ..models import PermitReplacement

class PermitReplacementAdmin(admin.ModelAdmin):
    list_display: Tuple[str, ...] = (
        'date_signed',
        'signature',
        'certificate_status',
    )
    search_fields: Tuple[str, ...] = ('certificate_status',)
    list_filter: Tuple[str, ...] = ('certificate_status', 'date_signed',)

admin.site.register(PermitReplacement, PermitReplacementAdmin)
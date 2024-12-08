from django.contrib import admin
from typing import Tuple
from ..models import PermitAppeal

class PermitAppealAdmin(admin.ModelAdmin):
    list_display: Tuple[str, ...] = (
        'reason_for_appeal',
        'appeal_type',
        'appeal_date',
    )
    search_fields: Tuple[str, ...] = ('reason_for_appeal', 'appeal_type')
    list_filter: Tuple[str, ...] = ('appeal_type', 'appeal_date')

admin.site.register(PermitAppeal, PermitAppealAdmin)
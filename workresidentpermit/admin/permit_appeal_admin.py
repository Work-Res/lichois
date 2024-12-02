from django.contrib import admin

from ..models import PermitAppeal

class PermitAppealAdmin(admin.ModelAdmin):
    list_display = (
        'reason_for_appeal',
        'appeal_type',
        'appeal_date',
    )
    search_fields = ('reason_for_appeal', 'appeal_type')
    list_filter = ('appeal_type', 'appeal_date')

admin.site.register(PermitAppeal, PermitAppealAdmin)
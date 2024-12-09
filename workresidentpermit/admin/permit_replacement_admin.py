from django.contrib import admin
from typing import Tuple
from ..models import PermitReplacement
from ..forms.work_resident_replacement_permit_form import WorkResReplacementPermitForm
from ..admin_site import workresidencepermit_admin


@admin.register(PermitReplacement, site=workresidencepermit_admin)
class PermitReplacementAdmin(admin.ModelAdmin):

    form = WorkResReplacementPermitForm
    list_display: Tuple[str, ...] = (
        'date_signed',
        'signature',
        'certificate_status',
    )
    search_fields: Tuple[str, ...] = ('certificate_status',)
    list_filter: Tuple[str, ...] = ('certificate_status', 'date_signed',)
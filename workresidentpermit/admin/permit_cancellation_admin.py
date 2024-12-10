from django.contrib import admin
from typing import Tuple

from base_module.admin_mixins import BaseUrlModelAdminMixin

from ..models import PermitCancellation
from ..forms.work_resident_cancellation_permit_form import WorkResPermitCancellationForm
from ..admin_site import workresidencepermit_admin



@admin.register(PermitCancellation, site=workresidencepermit_admin)
class PermitCancellationAdmin(BaseUrlModelAdminMixin, admin.ModelAdmin):
    form = WorkResPermitCancellationForm
    list_display: Tuple[str, ...] = (
        'submitter_type',
        'submitted_by',
        'cancellation_reasons',
    )
    search_fields: Tuple[str, ...] = (
        'submitter_type',
        'submitted_by',
    )

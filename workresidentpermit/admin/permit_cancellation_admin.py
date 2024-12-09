from django.contrib import admin
from ..models import PermitCancellation
from ..forms.work_resident_cancellation_permit_form import WorkResPermitCancellationForm
from typing import Tuple


class PermitCancellationAdmin(admin.ModelAdmin):
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

admin.site.register(PermitCancellation, PermitCancellationAdmin)
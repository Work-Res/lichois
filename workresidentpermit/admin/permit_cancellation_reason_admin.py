from django.contrib import admin
from ..models import PermitCancellationReason
from typing import Tuple
from ..forms.work_resident_cancellation_permit_form import WorkResCancellationPermitForm

class PermitCancellationReasonAdmin(admin.ModelAdmin):

	form = WorkResCancellationPermitForm
	list_display: Tuple[str, ...] = ('reason_for_cancellation', 'other_reason', 'created', 'modified',)
	search_fields: Tuple[str, ...] = ('reason_for_cancellation',)

admin.site.register(PermitCancellationReason, PermitCancellationReasonAdmin)

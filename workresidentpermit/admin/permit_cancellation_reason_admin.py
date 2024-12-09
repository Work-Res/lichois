from django.contrib import admin
from ..models import PermitCancellationReason
from typing import Tuple
from ..forms.cancellation_reason_form import WorkResPermitCancellationReasonForm
from ..admin_site import workresidencepermit_admin


@admin.register(PermitCancellationReason, site=workresidencepermit_admin)
class PermitCancellationReasonAdmin(admin.ModelAdmin):

	form = WorkResPermitCancellationReasonForm
	list_display: Tuple[str, ...] = ('reason_for_cancellation', 'other_reason', 'created', 'modified',)
	search_fields: Tuple[str, ...] = ('reason_for_cancellation',)


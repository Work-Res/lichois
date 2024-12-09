from django.contrib import admin
from ..models import PermitCancellationReason
from typing import Tuple
from ..forms.cancellation_reason_form import WorkResPermitCancellationReasonForm

class PermitCancellationReasonAdmin(admin.ModelAdmin):

	form = WorkResPermitCancellationReasonForm
	list_display: Tuple[str, ...] = ('reason_for_cancellation', 'other_reason', 'created', 'modified',)
	search_fields: Tuple[str, ...] = ('reason_for_cancellation',)

admin.site.register(PermitCancellationReason, PermitCancellationReasonAdmin)

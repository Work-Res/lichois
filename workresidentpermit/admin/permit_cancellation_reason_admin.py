from django.contrib import admin
from ..models import PermitCancellationReason
from typing import Tuple

class PermitCancellationReasonAdmin(admin.ModelAdmin):
	list_display: Tuple[str, ...] = ('reason_for_cancellation', 'created', 'modified',)
	search_fields: Tuple[str, ...] = ('reason_for_cancellation',)

admin.site.register(PermitCancellationReason, PermitCancellationReasonAdmin)

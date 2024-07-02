from django.contrib import admin
from ..models import PermitCancellationReason


class PermitCancellationReasonAdmin(admin.ModelAdmin):
	list_display = ('reason_for_cancellation', 'created', 'modified',)
	search_fields = ('reason_for_cancellation',)


admin.site.register(PermitCancellationReason, PermitCancellationReasonAdmin)

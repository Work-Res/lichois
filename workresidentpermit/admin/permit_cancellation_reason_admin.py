from django.contrib import admin
from ..models import PermitCancellationReason


@admin.register(PermitCancellationReason)
class PermitCancellationReasonAdmin(admin.ModelAdmin):
    list_display = ('reason_for_cancellation', 'created_at', 'updated_at')
    search_fields = ('reason_for_cancellation',)

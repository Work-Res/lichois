from django.contrib import admin
from app_payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin interface for the Payment model.
    """
    list_display = (
        'id',
        'reference_number',
        'transaction_id',
        'amount',
        'status',
        'payment_date',
        'tenant_id',
    )
    list_filter = ('status', 'payment_date')
    search_fields = ('reference_number', 'transaction_id', 'description')
    ordering = ('-payment_date',)
    readonly_fields = ('transaction_uuid',)

    fieldsets = (
        (None, {
            'fields': ('reference_number', 'transaction_id', 'transaction_uuid', 'status', 'amount')
        }),
        ('Additional Details', {
            'fields': ('description', 'payment_narration', 'cancellation_reason', 'address', 'tenant_id')
        }),
        ('Dates', {
            'fields': ('payment_date',)
        }),
    )

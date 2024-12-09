import uuid

from django.db import models
from django.utils.timezone import now

from app.models import ApplicationBaseModel


class Payment(ApplicationBaseModel):
    STATUS_PAID = 'PAID'
    STATUS_FAILED = 'FAILED'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_PENDING = 'PENDING'

    STATUS_CHOICES = [
        (STATUS_PAID, 'Paid'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_PENDING, 'Pending'),
    ]

    tenant_id = models.CharField(max_length=255, null=True, blank=True, default="Cybersource")

    transaction_id = models.CharField(max_length=255, null=True, blank=True)

    transaction_uuid = models.CharField(max_length=32, unique=True, default=uuid.uuid4().hex)

    payment_date = models.DateField(null=True, blank=True, default=now())

    status = models.CharField(choices=STATUS_CHOICES, max_length=100, null=True, blank=True)

    amount = models.DecimalField(max_digits=20, decimal_places=2)

    description = models.TextField(null=True, blank=True)

    reference_number = models.CharField(max_length=150, unique=True)

    payment_narration = models.TextField(null=True, blank=True)

    cancellation_reason = models.TextField(null=True, blank=True)

    address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"Payment {self.reference_number or self.transaction_id}"

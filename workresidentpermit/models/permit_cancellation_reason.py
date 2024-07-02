from django.db import models

from app.models import ApplicationBaseModel


class PermitCancellationReason(ApplicationBaseModel):
    reason_for_cancellation = models.CharField(max_length=255)
    other_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.reason_for_cancellation

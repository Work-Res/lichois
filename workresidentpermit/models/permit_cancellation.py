from django.db import models

from app.models import ApplicationBaseModel
from ..choices import SUBMITTER_TYPE


class PermitCancellation(ApplicationBaseModel):

    submitter_type = models.CharField(max_length=200, choices=SUBMITTER_TYPE)

    submitted_by = models.CharField(max_length=150, blank=True, null=True)

    cancellation_reasons = models.TextField(verbose_name="Give reasons to why you are cancelling your permit")

    class Meta:
        verbose_name = "Permit Cancellation"

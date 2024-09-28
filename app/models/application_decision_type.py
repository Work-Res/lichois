from django.db import models
from django.utils import timezone

from base_module.model_mixins import BaseUuidModel


class ApplicationDecisionType(BaseUuidModel):

    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=250)
    process_types = models.CharField(max_length=250)
    valid_from = models.DateField(default=timezone.now)
    valid_to = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Application Decision Type"
        ordering = ["-created"]

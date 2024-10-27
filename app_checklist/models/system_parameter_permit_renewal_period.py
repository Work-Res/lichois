from decimal import Decimal

from base_module.model_mixins import BaseUuidModel
from django.db import models


class SystemParameterPermitRenewalPeriod(BaseUuidModel):

    percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                  default=Decimal('0.25'))

    application_type = models.CharField(max_length=150)
    valid_from = models.DateField(auto_now=True)
    valid_to = models.DateField(null=True, blank=True, auto_now_add=True)

    class Meta:
        db_table = "system_parameter_permit_renewal"
        verbose_name = "System Parameter Period Renewal"
        verbose_name_plural = "System Parameter Period Renewal"

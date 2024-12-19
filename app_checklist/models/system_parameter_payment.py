from base_module.model_mixins import BaseUuidModel
from django.db import models


class SystemParameterPayment(BaseUuidModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    application_type = models.CharField(max_length=255)
    valid_from = models.DateField(auto_now=True)
    valid_to = models.DateField(null=True, blank=True, auto_now_add=True)

    class Meta:
        db_table = "system_parameter_payments"
        verbose_name = "System Parameter Payment"
        verbose_name_plural = "System Parameters"

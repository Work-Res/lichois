from django.db import models
from ..choices import CURRENCY_CHOICES
from base_module.model_mixins import BaseUuidModel

class CurrencyAmount(BaseUuidModel):
    currency_code = models.CharField(max_length=10, choices=CURRENCY_CHOICES, blank=True,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)

    class Meta:
        app_label = 'visa'

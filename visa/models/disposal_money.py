from django.db import models
from base_module.model_mixins import BaseUuidModel
from .visa_application import VisaApplication


class DisposalMoney(BaseUuidModel):

    visa_application = models.ForeignKey(
        VisaApplication,
        on_delete=models.CASCADE
    )

    disposal_money_currency = models.CharField(
        max_length=5
    )

    disposal_money_currency_other = models.CharField(
        max_length=5
    )

    disposal_money_currency_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        app_label = 'visa'
        unique_together = ('visa_application', 'disposal_money_currency')

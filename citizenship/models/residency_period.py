from django.db import models
from base_module.model_mixins import BaseUuidModel


class ResidencyPeriod(BaseUuidModel):

    period_from = models.DateField()
    period_until = models.DateField()
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Residency from {self.period_from} to {self.period_until}"

    @property
    def duration(self):
        """Returns the duration of the residency period."""
        return self.period_until - self.period_from

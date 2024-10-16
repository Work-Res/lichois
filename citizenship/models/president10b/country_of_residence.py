from django.db import models

from base_module.model_mixins import BaseUuidModel


class CountryOfResidence(BaseUuidModel):
    country = models.CharField(max_length=100)
    period_from = models.DateField()
    period_until = models.DateField()

    def __str__(self):
        return f"Residence in {self.country} from {self.period_from} to {self.period_until}"

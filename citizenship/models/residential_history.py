from django.db import models
from base_module.model_mixins import BaseUuidModel
from django.core.exceptions import ValidationError


class ResidentialHistory(BaseUuidModel):
    country = models.CharField(max_length=255, null=True, blank=True)
    residence_from_date = models.DateField(auto_now=True)
    residence_to_date = models.DateField(auto_now=True)

    class Meta:
        app_label = 'citizenship'

    def clean(self):
        if self.residence_to_date < self.residence_from_date:
            raise ValidationError("Residence to date must be after residence from date.")

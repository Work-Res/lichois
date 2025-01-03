from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class ResidentialHistoryModelMixin(models.Model):
    country = models.CharField(max_length=255, null=True, blank=True)
    residence_from_date = models.DateField(auto_now=True)
    residence_to_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True

    def clean(self):
        if self.residence_to_date < self.residence_from_date:
            raise ValidationError("Residence to date must be after residence from date.")

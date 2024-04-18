from django.db import models

from base_module.model_mixins import BaseUuidModel


class Country(BaseUuidModel):
    name = models.CharField(max_length=255)
    iso_code = models.CharField(max_length=2)
    iso_a2_code = models.CharField(max_length=2)
    iso_a3_code = models.CharField(max_length=3)
    cso_code = models.CharField(max_length=3)
    local = models.BooleanField(default=False)
    valid_from = models.DateField()
    valid_to = models.DateField()
    version = models.BigIntegerField()

    def __str__(self):
        return self.name

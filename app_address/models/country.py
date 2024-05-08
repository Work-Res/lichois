from django.db import models

from base_module.model_mixins import BaseUuidModel


class Country(BaseUuidModel):
    name = models.CharField(max_length=255)
    iso_code = models.CharField(max_length=2, null=True, blank=True)
    iso_a2_code = models.CharField(max_length=2, null=True, blank=True)
    iso_a3_code = models.CharField(max_length=3, null=True, blank=True)
    cso_code = models.CharField(max_length=3, null=True, blank=True)
    local = models.BooleanField(default=False)
    valid_from = models.DateField(auto_now=True)
    valid_to = models.DateField(null=True)

    def __str__(self):
        return self.name

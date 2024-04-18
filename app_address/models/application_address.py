from django.db import models

from base_module.model_mixins import BaseUuidModel


from app.models.application_version import ApplicationVersion
from .country import Country


class ApplicationAddress(BaseUuidModel):

    apartment_number = models.CharField(max_length=100)
    plot_number = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    address_type = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    private_bag = models.CharField(max_length=100)
    po_box = models.CharField(max_length=100)
    application_version = models.ForeignKey(ApplicationVersion, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.apartment_number}, {self.plot_number}, {self.street_address}, {self.city}, {self.country}"

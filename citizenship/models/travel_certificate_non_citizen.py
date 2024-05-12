from django.db import models
from base_module.model_mixins import BaseUuidModel


class TravelCertNonCitizen(BaseUuidModel):

    #personal_details
    #original_home_address
    nationality = models.CharField(max_length=250)
    kraal_head_names = models.CharField(max_length=250, blank=True, null=True)
    chief_names = models.CharField(max_length=250, blank=True, null=True)
    application_date = models.DateField()
    signature = models.CharField(max_length=250, blank=True, null=True)
    issuing_authority = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = ''
        app_label = 'citizenship'

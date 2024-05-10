from django.db import models
from base_module.model_mixins import BaseUuidModel


class DCCertificate(BaseUuidModel):

    dc_surname = models.CharField(max_length=190)
    dc_firstname = models.CharField(max_length=190)
    # TODO: declarant_id
    settlement_year = models.DateField()
    origin_country = models.CharField(max_length=150)
    community = models.CharField(max_length=150)
    declaration_place = models.TextField(max_length=150)
    declaration_datetime = models.DateTimeField()
    dc_sign = models.CharField(max_length=150)

    class Meta:
        app_label = 'citizenship'

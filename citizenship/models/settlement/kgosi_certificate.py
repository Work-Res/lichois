from django.db import models
from base_module.model_mixins import BaseUuidModel


class KgosiCertificate(BaseUuidModel):

    document_number = models.CharField(max_length=100, null=True, blank=True)

    kgosi_surname = models.CharField(max_length=190)

    kgosi_firstname = models.CharField(max_length=190)

    village = models.CharField(max_length=150)

    tribe = models.CharField(max_length=150)

    #TODO: declarant_id
    known_year = models.DateField()

    community = models.CharField(max_length=150)

    living_circumstance = models.TextField(max_length=150)

    class Meta:
        app_label = 'citizenship'

from django.db import models
from base_module.model_mixins import BaseUuidModel


class KgosanaCertificate(BaseUuidModel):

    document_number = models.CharField(max_length=100, null=True, blank=True)
    kgosana_surname = models.CharField(max_length=190)
    kgosana_firstname = models.CharField(max_length=190)
    id_elder_firstname = models.CharField(max_length=150)
    id_elder_lastname = models.CharField(max_length=150)
    community = models.CharField(max_length=150)
    settlement_year = models.DateField()
    certificate_place = models.TextField(max_length=150)
    certificate_datetime = models.DateTimeField()
    kgosana_sign = models.CharField(max_length=150)

    class Meta:
        app_label = 'citizenship'

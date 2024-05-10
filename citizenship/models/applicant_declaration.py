from base_module.model_mixins import BaseUuidModel
from django.db import models


class ApplicantDeclaration(BaseUuidModel):

    declarant_surname = models.CharField(max_length=150, blank=True, null=True)
    declarant_middlename = models.CharField(max_length=150, blank=True, null=True)
    declarant_firstname = models.CharField(max_length=150, blank=True, null=True)
    declarant_maidenname = models.CharField(max_length=150, blank=True, null=True)
    declarant_signature = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        app_label = 'citizenship'

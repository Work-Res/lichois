from django.db import models
from base_module.model_mixins import BaseUuidModel, DeclarationModelMixin
from app.models import ApplicationBaseModel
from app_address.models import ApplicationAddress

class TravelCertificate(BaseUuidModel):
    document_number = models.ForeignKey(ApplicationBaseModel, on_delete=models.CASCADE)
    og_home_address_id = models.ForeignKey(ApplicationAddress, on_delete=models.CASCADE)
    kraal_head_name = models.CharField(max_length=200)
    chief_name = models.CharField(max_length=200)
    clan_name = models.CharField(max_length=200)
    date = models.DateField()
    applicant_signature = models.ForeignKey(DeclarationModelMixin, on_delete=models.CASCADE)
    issuing_authority_signature = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Travel Certificate'
        verbose_name_plural = 'Travel Certificates'
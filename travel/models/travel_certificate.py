from django.db import models
from base_module.model_mixins import BaseUuidModel, DeclarationModelMixin
from app.models import ApplicationBaseModel
from app_address.models import ApplicationAddress


class TravelCertificate(ApplicationBaseModel):
	kraal_head_name = models.CharField(max_length=200)
	chief_name = models.CharField(max_length=200)
	clan_name = models.CharField(max_length=200)
	date = models.DateField(auto_now=True)
	applicant_signature = models.CharField(max_length=200)
	issuing_authority_signature = models.CharField(max_length=200, null=True, blank=True)
	
	class Meta:
		verbose_name = 'Travel Certificate'
		verbose_name_plural = 'Travel Certificates'

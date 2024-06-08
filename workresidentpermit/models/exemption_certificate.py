from django.db import models
from app.models import ApplicationBaseModel


class ExemptionCertificate(ApplicationBaseModel):
	
	business_name = models.CharField(max_length=150)
	employment_capacity = models.CharField(max_length=250)
	proposed_period = models.PositiveIntegerField()
	status = models.CharField(max_length=250)
	applicant_signature = models.TextField(max_length=250)
	application_date = models.DateField()
	commissioner_signature = models.CharField(max_length=250)
	
	class Meta:
		verbose_name = 'Exemption Certificate'

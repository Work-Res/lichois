from django.db import models
from base_module.model_mixins import BaseUuidModel


class ExemptionCertificate(BaseUuidModel):

	# personal_information
	# passport_details

	business_name = models.CharField(max_length=150)
	# address?
	employment_capacity = models.CharField(max_length=250)
	proposed_period = models.PositiveIntegerField()
	status = models.CharField(max_length=250)
	applicant_signature = models.TextField(max_length=250)
	application_date = models.DateField()
	commissioner_signature = models.CharField(max_length=250)

	class Meta:
		app_label = 'work_residence_permit'

from django.db import models
from base_module.model_mixins import BaseUuidModel
from .recruiters_licence import RecruitersLicense
from .wage_rates import WageRate


class PotentialEmployer(BaseUuidModel):

	recruiters_license = models.ForeignKey(RecruitersLicense, on_delete=models.CASCADE)
	firstname = models.CharField(max_length=150)
	lastname = models.CharField(max_length=150)
	position = models.CharField(max_length=150)
	salary_rate = models.ForeignKey(WageRate, on_delete=models.CASCADE)

	#physical_address
	#postal_address
	#contacts

	class Meta:
		app_label = 'workresidentpermit'

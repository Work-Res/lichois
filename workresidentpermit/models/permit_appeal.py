from django.db import models
from base_module.model_mixins import BaseUuidModel


class PermitAppeal(BaseUuidModel):
	reason_for_appeal = models.TextField()
	appeal_date = models.DateField(auto_now_add=True)
	
	class Meta:
		verbose_name = 'Work Residence Permit Appeal'
		verbose_name_plural = 'Work Residence Permit Appeals'

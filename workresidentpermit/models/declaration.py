from django.db import models

from base_module.model_mixins import BaseUuidModel


class Declaration(BaseUuidModel):
	declaration_fname = models.CharField(
		verbose_name='Declaration firstname',
		max_length=150
	)
	
	declaration_lname = models.CharField(
		verbose_name='Declaration lastname',
		max_length=150
	)
	
	declaration_date = models.DateField(
		#validation=date_not_future
	)
	
	signature = models.CharField(max_length=190)
	
	# work_resident_permit = models.ForeignKey(ResidencePermit, on_delete=models.CASCADE)
	
	class Meta:
		verbose_name = 'Declaration'

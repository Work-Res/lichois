from django.db import models

from base_module.model_mixins import BaseUuidModel

from ..models import WorkResidencePermit


class Permit(BaseUuidModel):

	permit_type = models.CharField(max_length=190) #, choices=PERMIT_TYPE)
	permit_no = models.CharField(max_length=190)
	date_issued = models.DateField()
	date_expiry = models.DateField()
	place_issue = models.CharField(max_length=190)
	work_resident_permit = models.ForeignKey(WorkResidencePermit, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Permit'

from django.db import models

from app.models import ApplicationBaseModel


class Permit(ApplicationBaseModel):

	permit_type = models.CharField(max_length=190) #, choices=PERMIT_TYPE)
	permit_no = models.CharField(max_length=190)
	date_issued = models.DateField()
	date_expiry = models.DateField()
	place_issue = models.CharField(max_length=190)

	class Meta:
		verbose_name = 'Permit'


from django.db import models
from app.models import ApplicationBaseModel

from ..choices import CERTIFICATE_STATUS


class DuplicateWorkPermit(ApplicationBaseModel):
	full_name = models.CharField(max_length=255)
	date_signed = models.DateField()
	signature = models.CharField(max_length=255)
	certificate_status = models.CharField(max_length=255, choices=CERTIFICATE_STATUS)
	
	class Meta:
		app_label = 'work_residence_permit'

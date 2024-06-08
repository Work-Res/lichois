from django.db import models

from app.models import ApplicationBaseModel
from app_attachments.models import ApplicationAttachment


class PermitCancellation(ApplicationBaseModel):

	attachments = models.ManyToManyField(ApplicationAttachment, blank=True)

	submitter_type = models.CharField(max_length=200, choices=['applicant', 'employer', 'officer'])

	submitted_by = models.CharField(max_length=150)
	
	class Meta:
		app_label = 'work_residence_permit'

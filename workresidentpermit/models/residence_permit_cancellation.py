from django.db import models

from app.models import ApplicationBaseModel
from app_attachments.models import ApplicationAttachment


class ResidencePermitCancellation(ApplicationBaseModel):
	attachments = models.ManyToManyField(ApplicationAttachment, blank=True)
	
	class Meta:
		app_label = 'work_residence_permit'

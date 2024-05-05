from django.db import models

from base_module.model_mixins import BaseUuidModel

from .work_resident_permit import WorkResidencePermit


class SecurityClearance(BaseUuidModel):

	work_resident_permit = models.ForeignKey(WorkResidencePermit, on_delete=models.CASCADE)

	date_requested = models.DateTimeField(auto_now_add=True)

	date_approved = models.DateTimeField()

	status = models.CharField(max_length=20, choices=[
		('pending', 'Pending'),
		('approved', 'Approved'),
		('rejected', 'Rejected'),
	])

	summary = models.TextField()

	class Meta:
		app_label = 'work_residence_permit'

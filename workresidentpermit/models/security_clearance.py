from django.db import models

from base_module.model_mixins import BaseUuidModel


class SecurityClearance(BaseUuidModel):

	document_id = models.CharField(max_length=190)

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

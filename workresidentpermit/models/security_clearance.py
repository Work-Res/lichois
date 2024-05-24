from django.db import models

from base_module.model_mixins import BaseUuidModel


class SecurityClearance(BaseUuidModel):

	document_id = models.CharField(max_length=190)

	document_number = models.CharField(max_length=100, null=True, blank=True)

	date_requested = models.DateTimeField(auto_now_add=True)

	date_approved = models.DateTimeField()

	status = models.CharField(max_length=20, choices=[
		('pending', 'Pending'),
		('approved', 'Approved'),
		('rejected', 'Rejected'),
	])

	summary = models.TextField()

	class Meta:
		verbose_name = 'Security Clearance'

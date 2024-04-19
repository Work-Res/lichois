from django.db import models

from base_module.model_mixins import BaseUuidModel

from base_module.choices import PREFERRED_METHOD_COMM, YES_NO, REASONS_PERMIT
from app.models import ApplicationVersion


class WorkResidencePermit(BaseUuidModel):

	file_number = models.CharField(max_length=190)
	preferred_method_comm = models.CharField(max_length=190, choices=PREFERRED_METHOD_COMM)
	preferred_method_comm_value = models.CharField(max_length=190)
	language = models.CharField(max_length=190)
	permit_reason = models.TextField(),
	state_period_required = models.DateField()
	propose_work_employment = models.CharField(max_length=4, choices=YES_NO)
	reason_applying_permit = models.CharField(max_length=190, choices=REASONS_PERMIT)
	documentary_proof = models.CharField(max_length=190)
	travelled_on_pass = models.CharField(max_length=190)
	is_spouse_applying_residence = models.CharField(max_length=190, choices=YES_NO)
	ever_prohibited = models.TextField()
	sentenced_before = models.TextField()
	entry_place = models.CharField(max_length=190)
	arrival_date = models.DateField()
	application_version = models.ForeignKey(ApplicationVersion, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Work Residence Permits'

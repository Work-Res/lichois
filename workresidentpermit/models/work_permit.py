from django.db import models
from base_module.choices import PERMIT_STATUS

from app.models import ApplicationBaseModel
from ..model_mixins import (EmployerModelMixin, TraineeModelMixin, InvestorModelMixin, EmploymentRecordModelMixin)
from .employer_record import EmploymentRecord


class WorkPermit(ApplicationBaseModel, EmployerModelMixin, TraineeModelMixin, InvestorModelMixin,
                 EmploymentRecordModelMixin):
	permit_status = models.CharField(max_length=50, choices=PERMIT_STATUS, default='pending')
	job_offer = models.TextField()
	qualification = models.CharField(max_length=255)
	years_of_study = models.IntegerField()
	
	class Meta:
		verbose_name = 'Work Permits'


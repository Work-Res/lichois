from django.db import models
from base_module.model_mixins import BaseUuidModel
from app.models import Application


class ApplicationBatch(BaseUuidModel):
	applications = models.ManyToManyField(Application)
	batch_type = models.CharField(max_length=100, blank=True, null=True)
	
	def __str__(self):
		return f'ApplicationBatch {self.batch_type} for Applications'

from django.db import models
from base_module.model_mixins import BaseUuidModel
from .application import Application


class ApplicationBatch(BaseUuidModel):
	batch_id = models.CharField(max_length=250)
	applications = models.ManyToManyField(Application)
	batch_type = models.CharField(max_length=100)
	batch_duration = models.DurationField()
	
	def __str__(self):
		return f'ApplicationBatch {self.batch_type} for Applications {self.application_ids}'

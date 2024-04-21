from django.db import models
from base_module.model_mixins import BaseUuidModel


class AgendaItem(BaseUuidModel):
	item_name = models.CharField(max_length=250)
	item_description = models.TextField()
	item_duration = models.DurationField()
	item_order = models.IntegerField()
	
	def __str__(self):
		return f'AgendaItem {self.item_name} for Agenda {self.agenda_id}'

from django.db import models
from base_module.model_mixins import BaseUuidModel
from .agenda import Agenda


class AgendaItem(BaseUuidModel):
	item_name = models.CharField(max_length=250)
	item_description = models.TextField()
	item_duration = models.PositiveIntegerField()
	item_order = models.IntegerField()
	agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
	
	def __str__(self):
		return f'AgendaItem {self.item_name} for Agenda {self.item_description}'

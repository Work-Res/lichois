from django.db import models
from base_module.model_mixins import BaseUuidModel


class Statement(BaseUuidModel, models.Model):
    statement_content = models.TextField()  
    statement_date = models.DateTimeField(auto_now_add=True)  
    made_by = models.CharField(max_length=255)
    related_prohibited_immigrant = models.ForeignKey('ProhibitedImmigrant', on_delete=models.SET_NULL, null=True, blank=True)
    additional_notes = models.TextField(null=True, blank=True)  
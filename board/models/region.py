from django.db import models
from base_module.model_mixins import BaseUuidModel


class Region(BaseUuidModel):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

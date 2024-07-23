from django.db import models

from base_module.model_mixins import BaseUuidModel


class Role(BaseUuidModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

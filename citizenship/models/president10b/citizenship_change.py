from django.db import models

from base_module.model_mixins import BaseUuidModel


class CitizenshipChange(BaseUuidModel):
    previous_citizenship = models.CharField(max_length=255)
    new_citizenship = models.CharField(max_length=255)
    date_of_change = models.DateField()

    def __str__(self):
        return f"Citizenship changed from {self.previous_citizenship} to {self.new_citizenship}"

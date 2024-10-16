from django.db import models
from app.models import ApplicationBaseModel


class NameChange(ApplicationBaseModel):
    previous_name = models.CharField(max_length=255)
    new_name = models.CharField(max_length=255)
    date_of_change = models.DateField()

    def __str__(self):
        return f"Name changed from {self.previous_name} to {self.new_name}"

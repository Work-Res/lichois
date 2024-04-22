from django.db import models

from base_module.model_mixins import BaseUuidModel

from .business_process import BusinessProcess


class Activity(BaseUuidModel):

    """
    Represents individual activities within the process (verification, committee review, decision making ) e.t.c
    """

    process = models.ForeignKey(BusinessProcess, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    valid_from = models.DateField()
    valid_to = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.process}"

from django.db import models

from base_module.model_mixins import BaseUuidModel


class OfficeLocationClassifier(BaseUuidModel):

    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    description = models.TextField()
    valid_from = models.DateField()
    valid_to = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name = "OfficeLocationClassifier"
        verbose_name_plural = "Office Location Classifiers"

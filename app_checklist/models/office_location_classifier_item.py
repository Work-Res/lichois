from django.db import models

from .office_location_classifier import OfficeLocationClassifier

from base_module.model_mixins import BaseUuidModel


class OfficeLocationClassifierItem(BaseUuidModel):

    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    description = models.TextField()
    office_location_classifier = models.ForeignKey(OfficeLocationClassifier, on_delete=models.CASCADE)
    valid_from = models.DateField()
    valid_to = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name = "OfficeLocationClassifierItem"
        verbose_name_plural = "Office Location ClassifierItems"

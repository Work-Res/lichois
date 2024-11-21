from django.db import models

from base_module.model_mixins import BaseUuidModel


class Classifier(BaseUuidModel):

    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    description = models.TextField()
    valid_from = models.DateField()
    valid_to = models.DateField()
    checksum = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name = "Classifier"
        verbose_name_plural = "Classifiers"

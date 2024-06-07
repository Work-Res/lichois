from django.db import models

from .checklist_classifier import ChecklistClassifier

from base_module.model_mixins import BaseUuidModel


class ChecklistClassifierItem(BaseUuidModel):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    application_type = models.CharField(max_length=100)
    description = models.TextField()
    mandatory = models.BooleanField(default=False)
    checklist_classifier = models.ForeignKey(ChecklistClassifier, on_delete=models.CASCADE)
    sequence = models.IntegerField(blank=True, null=True)
    valid_from = models.DateField()
    valid_to = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name = "ChecklistClassifier"
        verbose_name_plural = "Checklist ClassifierItems"

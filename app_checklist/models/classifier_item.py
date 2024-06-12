from django.db import models

from .classifier import Classifier

from base_module.model_mixins import BaseUuidModel


class ClassifierItem(BaseUuidModel):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    process = models.CharField(max_length=100)
    description = models.TextField()
    mandatory = models.BooleanField(default=False)
    classifier = models.ForeignKey(Classifier, on_delete=models.CASCADE)
    sequence = models.IntegerField(blank=True, null=True)
    create_task_rules = models.TextField()
    valid_from = models.DateField()
    valid_to = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name = "ClassifierItem"
        verbose_name_plural = "Classifier Items"

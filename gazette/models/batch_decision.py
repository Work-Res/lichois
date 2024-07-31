
from django.db import models
from .batch import Batch
from .choices import BATCH_DECISION_CHOICES
from base_module.model_mixins import BaseUuidModel


class BatchDecision(BaseUuidModel):

    batch = models.OneToOneField(Batch, related_name='decision', on_delete=models.CASCADE)
    decision = models.CharField(max_length=20, choices=BATCH_DECISION_CHOICES, default='APPROVED')
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Decision on {self.batch.title} by {self.created_by.username}"

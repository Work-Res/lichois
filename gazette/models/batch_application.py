from django.db import models

from app.models import Application
from .batch import Batch
from base_module.model_mixins import BaseUuidModel


class BatchApplication(BaseUuidModel):
    batch = models.ForeignKey(Batch, related_name='batch_applications', on_delete=models.CASCADE)
    application = models.ForeignKey(Application, related_name='batch_applications', on_delete=models.CASCADE)
    included_in_final_list = models.BooleanField(default=False)
    decision_notes = models.TextField(blank=True, null=True)
    reviewed_by_legal = models.BooleanField(default=False)
    reviewed_by_ag = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['batch', 'application'], name='unique_batch_application')
        ]

    def __str__(self):
        return f'{self.application.applicant_name} - {self.batch.name}'

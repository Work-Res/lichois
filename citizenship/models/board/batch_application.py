from django.db import models

from app.models import Application
from .batch import Batch
from .meeting_session import MeetingSession
from base_module.model_mixins import BaseUuidModel
from django.core.exceptions import ValidationError


class BatchApplication(BaseUuidModel):
    batch = models.ForeignKey(Batch, related_name='applications', on_delete=models.CASCADE)
    application = models.ForeignKey(Application, related_name='batches', on_delete=models.CASCADE)
    meeting_session = models.ForeignKey(MeetingSession, related_name='meeting_sessions', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.application.application_document.document_number} - {self.batch.name}'

    def save(self, *args, **kwargs):
        if BatchApplication.objects.filter(application=self.application).exists():
            raise ValidationError(f'Application {self.application} is already added to another batch.')
        super().save(*args, **kwargs)

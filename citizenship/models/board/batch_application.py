from django.db import models

from app.models import Application
from .batch import Batch
from .meeting_session import MeetingSession


class BatchApplication(models.Model):
    batch = models.ForeignKey(Batch, related_name='applications', on_delete=models.CASCADE)
    application = models.ForeignKey(Application, related_name='batches', on_delete=models.CASCADE)
    meeting_session = models.ForeignKey(MeetingSession, related_name='sessions', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.application.applicant_name} - {self.batch.name}'

from django.db import models
from django.utils import timezone

from base_module.model_mixins import BaseUuidModel

from citizenship.models import MeetingSession


class ConflictOfInterestDuration(BaseUuidModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('open', 'Open'),
        ('completed', 'Completed')
    ]

    meeting_session = models.OneToOneField(MeetingSession, related_name='duration', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def is_within_duration(self):
        current_time = timezone.now()
        return self.start_time <= current_time <= self.end_time

    def __str__(self):
        return f"From {self.start_time} to {self.end_time} for session {self.meeting_session}"

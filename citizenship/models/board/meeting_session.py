from django.db import models
from .meeting import Meeting

from base_module.model_mixins import BaseUuidModel


class MeetingSession(BaseUuidModel):
    meeting = models.ForeignKey(Meeting, related_name='board_meeting', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    batch_application_complete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} on {self.date} from {self.start_time} to {self.end_time}'

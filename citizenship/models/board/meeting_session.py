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

    def get_duration(self):
        # Convert TimeField objects to datetime objects with today's date
        from datetime import datetime, timedelta

        # Assuming the same day for start and end time
        today = datetime.today().date()
        start_datetime = datetime.combine(today, self.start_time)
        end_datetime = datetime.combine(today, self.end_time)

        # Calculate the difference
        if end_datetime >= start_datetime:
            duration = end_datetime - start_datetime
        else:
            # If end_time is on the next day, add a day to end_datetime
            end_datetime = datetime.combine(today + timedelta(days=1), self.end_time)
            duration = end_datetime - start_datetime

        return duration

    def __str__(self):
        return f'{self.title} on {self.date} from {self.start_time} to {self.end_time}'

from django.db import models

from citizenship.models.board.meeting import Meeting


class Batch(models.Model):
    meeting = models.ForeignKey(Meeting, related_name='batches', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} - {self.meeting.title}'

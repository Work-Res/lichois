from django.db import models

from app.models import Application

from .attendee import Attendee


class ConflictOfInterest(models.Model):
    attendee = models.ForeignKey(Attendee, related_name='conflicts', on_delete=models.CASCADE)
    application = models.ForeignKey(Application, related_name='conflicts', on_delete=models.CASCADE)
    has_conflict = models.BooleanField(default=True)
    declared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.attendee.member.user.username} - {self.application.document_number}'

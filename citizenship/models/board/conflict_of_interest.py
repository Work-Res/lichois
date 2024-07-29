from django.db import models

from app.models import Application

from .attendee import Attendee

from .managers.conflict_of_interest_manager import ConflictOfInterestManager
from base_module.model_mixins import BaseUuidModel


class ConflictOfInterest(BaseUuidModel):
    attendee = models.ForeignKey(Attendee, related_name='conflicts', on_delete=models.CASCADE)
    application = models.ForeignKey(Application, related_name='conflicts', on_delete=models.CASCADE)
    has_conflict = models.BooleanField(default=True)
    declared_at = models.DateTimeField(auto_now_add=True)
    objects = ConflictOfInterestManager()

    def __str__(self):
        return f'{self.attendee.member.user.username} - {self.application.document_number}'

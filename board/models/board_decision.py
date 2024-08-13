from django.db import models
from base_module.model_mixins import BaseUuidModel
from app.models import Application
from .board_meeting import BoardMeeting
from ..choices import DECISION_OUTCOME


class BoardDecision(BaseUuidModel):

    board_meeting = models.ForeignKey(BoardMeeting, on_delete=models.CASCADE)
    assessed_application = models.OneToOneField(Application, on_delete=models.CASCADE)
    vetting_outcome = models.TextField(null=True, blank=True)
    decision_outcome = models.CharField(choices=DECISION_OUTCOME, max_length=15)
    outcome_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.assessed_application}"

    class Meta:
        app_label = "board"

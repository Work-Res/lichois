from django.db import models
from base_module.model_mixins import BaseUuidModel
from app.models import Application
from app.models.application_base_model import ApplicationBaseModel
from .board_meeting import BoardMeeting
from ..choices import DECISION_OUTCOME


class BoardDecision(ApplicationBaseModel):

    board_meeting = models.ForeignKey(BoardMeeting, on_delete=models.CASCADE)
    vetting_outcome = models.TextField(null=True, blank=True)
    decision_outcome = models.CharField(choices=DECISION_OUTCOME, max_length=15)
    outcome_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.document_number} - {self.decision_outcome}"

    def to_dict(self):
        return {
            "board_meeting": self.board_meeting.title,
            "document_number": self.document_number,
            "vetting_outcome": self.vetting_outcome,
            "decision_outcome": self.decision_outcome,
            "outcome_reason": self.outcome_reason,
        }

    class Meta:
        app_label = "board"

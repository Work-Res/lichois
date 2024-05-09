from django.db import models
from .application_base_model import ApplicationBaseModel
from ..choices import DECISION_OUTCOME
from app_comments.models import Comment


class ApplicationVerification(ApplicationBaseModel):

    decision = models.CharField(choices=DECISION_OUTCOME, max_length=15)
    outcome_reason = models.TextField(null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.decision}'

    class Meta:
        app_label = 'app'

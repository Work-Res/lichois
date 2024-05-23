from django.db import models
from .application_base_model import ApplicationBaseModel
from app_comments.models import Comment

from app_decision.models import ApplicationDecisionType


class ApplicationVerification(ApplicationBaseModel):

    decision = models.ForeignKey(ApplicationDecisionType, on_delete=models.SET_NULL, null=True)
    outcome_reason = models.TextField(null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.decision}'

    class Meta:
        app_label = 'app'

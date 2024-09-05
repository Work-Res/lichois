
from django.db import models

from app.models import ApplicationBaseModel

from .application_decision_type import ApplicationDecisionType
from app_comments.models import Comment


class ApplicationDecision(ApplicationBaseModel):

    final_decision_type = models.ForeignKey(ApplicationDecisionType, on_delete=models.CASCADE,
                                            related_name='final_decision_type', null=True, blank=True)

    proposed_decision_type = models.ForeignKey(ApplicationDecisionType, on_delete=models.CASCADE,
                                               related_name='proposed_decision_type', null=True, blank=True)

    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Application Decision"
        ordering = ['-created']

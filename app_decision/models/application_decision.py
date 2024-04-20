
from django.db import models

from app.models import ApplicationBaseModel

from .application_decision_type import ApplicationDecisionType


def app_doc_default():
    return {}


class ApplicationDecision(ApplicationBaseModel):

    decision_type = models.ForeignKey(ApplicationDecisionType, on_delete=models.CASCADE, related_name='decision_type')
    proposed_decision_type = models.ForeignKey(ApplicationDecisionType, on_delete=models.CASCADE,
                                               related_name='proposed_decision_type')

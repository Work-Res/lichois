
from django.db import models

from base_module.model_mixins import BaseUuidModel
from app.models.application_version import ApplicationVersion

from .application_decision_type import ApplicationDecisionType


class ApplicationDecision(BaseUuidModel):

    decision_type = models.ForeignKey(ApplicationDecisionType, on_delete=models.CASCADE)
    proposed_decision_type = models.ForeignKey(ApplicationDecisionType, on_delete=models.CASCADE)
    application_version = models.ForeignKey(ApplicationVersion, on_delete=models.CASCADE)
    application_document = models.JSONField("application_document", default={})

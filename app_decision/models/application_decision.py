
from django.db import models
# from django.contrib.postgres.fields import JSONField

from base_module.model_mixins import BaseUuidModel
from app.models.application_version import ApplicationVersion

from .application_decision_type import ApplicationDecisionType


def app_doc_default():
    return {}


class ApplicationDecision(BaseUuidModel):

    decision_type = models.ForeignKey(ApplicationDecisionType, on_delete=models.CASCADE, related_name='decision_type')
    proposed_decision_type = models.ForeignKey(ApplicationDecisionType, on_delete=models.CASCADE,
                                               related_name='proposed_decision_type')
    application_version = models.ForeignKey(ApplicationVersion, on_delete=models.CASCADE)
    #application_document = JSONField("application_document", default=app_doc_default)

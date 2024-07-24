import logging


from app.models import Application

from app_comments.models import Comment
from app.models import CommissionerDecision

from workresidentpermit.workflow import RecommendationTransitionData

from .application_decision_service import ApplicationDecisionService


class ExemptionCertificateDecisionService(ApplicationDecisionService):
    """Responsible for creation of commissioner recommendation exemption certificate decision."""

    def __init__(self, document_number, comment: Comment = None):
        self.document_number = document_number
        self.comment = comment
        super().__init__(document_number=document_number, comment=comment)
        self.application = Application.objects.get(
            application_document__document_number=document_number
        )
        self.workflow = RecommendationTransitionData()

    def decision_predicate(self):
        return True

    def next_flow_activity(self):
        """Determine the next flow activity not based on any decision made."""
        self.run_workflow(application=self.application, workflow=self.workflow)

from app.models import Application
from app_comments.models import Comment
from app_decision.services import ApplicationDecisionService
from citizenship.utils import VerificationProcessWhenCompletedIsRequiredForProduction


class VerificationProductionDecisionService(ApplicationDecisionService):
    """Responsible for creation of commissioner recommendation exemption certificate decision."""

    def __init__(self, document_number, comment: Comment = None, decision_value=None):
        self.document_number = document_number
        self.comment = comment
        self.decision_value = decision_value
        super().__init__(document_number=document_number, comment=comment, decision_value=decision_value)
        self.application = Application.objects.get(
            application_document__document_number=document_number
        )

    def decision_predicate(self):
        if (
            self.application.application_type
            in VerificationProcessWhenCompletedIsRequiredForProduction.configured_process()
        ):
            return True
        return False

    def next_flow_activity(self):
        """Determine the next flow activity not based on any decision made."""
        pass

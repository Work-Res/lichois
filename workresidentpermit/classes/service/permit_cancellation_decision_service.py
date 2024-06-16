
import logging

from app.models import Application
from app.utils import ApplicationDecisionEnum

from app_comments.models import Comment
from workresidentpermit.models import MinisterDecision


from workresidentpermit.workflow import ProductionTransactionData

from .application_decision_service import ApplicationDecisionService
from ...utils import WorkResidentPermitApplicationTypeEnum


class PermitCancellationDecisionService(ApplicationDecisionService):

    def __init__(self, document_number, comment: Comment = None, minister_decision: MinisterDecision = None):
        self.document_number = document_number
        self.comment = comment
        super().__init__(document_number=document_number, comment=comment)
        self._minister_decision = minister_decision
        self.application = Application.objects.get(application_document__document_number=document_number)
        self.workflow = ProductionTransactionData()
        self.logger = logging.getLogger(__name__)

    def minister_decision(self):
        if not self._minister_decision:
            try:
                self._minister_decision = MinisterDecision.objects.get(
                    document_number=self.document_number
                )
            except MinisterDecision.DoesNotExist:
                pass
        else:
            return self._minister_decision

    def decision_predicate(self):
        is_minister_decision = False
        cancellation_types = [
            e.name.upper() for e in WorkResidentPermitApplicationTypeEnum if "CANCELLATION" in e.name]

        if self.application.application_type.upper() in cancellation_types:
            minister_decision = self.minister_decision()
            if minister_decision:
                is_minister_decision = minister_decision.status.code.lower() == \
                                       ApplicationDecisionEnum.ACCEPTED.value.lower()

            if is_minister_decision:
                self.decision_value = ApplicationDecisionEnum.ACCEPTED.value
                self.workflow.minister_decision = ApplicationDecisionEnum.ACCEPTED.value
                return True
            elif minister_decision:
                self.decision_value = ApplicationDecisionEnum.REJECTED.value
                self.workflow.minister_decision = ApplicationDecisionEnum.REJECTED.value
                return True
            else:
                self.logger.info(
                    "Application decision cannot be completed, application cancellation.")

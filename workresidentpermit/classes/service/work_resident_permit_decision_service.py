import logging

from app.models import Application, SecurityClearance
from app.utils import ApplicationDecisionEnum
from app_comments.models import Comment
from app_decision.services import ApplicationDecisionService
from board.models import BoardDecision

from ...workflow import ProductionTransactionData


class WorkResidentPermitDecisionService(ApplicationDecisionService):
    """Responsible for create application decision based on security clearance or board decision."""

    def __init__(
        self,
        document_number,
        security_clearance: SecurityClearance = None,
        board_decision: BoardDecision = None,
        comment: Comment = None,
    ):
        self.document_number = document_number
        self.comment = comment
        super().__init__(document_number=document_number, comment=comment)
        self._board_decision = board_decision
        self._security_clearance = security_clearance
        self.application = Application.objects.get(
            application_document__document_number=document_number
        )
        self.workflow = ProductionTransactionData()
        self.logger = logging.getLogger(__name__)

    def update_application(self):
        application = Application.objects.get(
            application_document__document_number=self.document_number
        )
        application.board = self._board_decision.decision_outcome
        application.save()

    def decision_predicate(self):
        is_security_clearance_accepted = False
        is_board_decision_taken = False

        security_clearance = self.security_clearance()
        if security_clearance:
            is_security_clearance_accepted = (
                security_clearance.status.code.lower()
                == ApplicationDecisionEnum.ACCEPTED.value.lower()
            )
        board_decision = self.board_decision()
        if board_decision:
            is_board_decision_taken = (
                self._board_decision.decision_outcome.lower()
                == ApplicationDecisionEnum.ACCEPTED.value.lower()
            )

        if is_security_clearance_accepted and is_board_decision_taken:
            self.decision_value = ApplicationDecisionEnum.ACCEPTED.value
            self.workflow.board_decision = (
                ApplicationDecisionEnum.ACCEPTED.value.upper()
            )
            self.workflow.security_clearance = (
                ApplicationDecisionEnum.ACCEPTED.value.upper()
            )
            return True
        elif self._board_decision and security_clearance:
            self.decision_value = ApplicationDecisionEnum.REJECTED.value
            self.workflow.board_decision = (
                ApplicationDecisionEnum.REJECTED.value.upper()
            )
            self.workflow.security_clearance = (
                ApplicationDecisionEnum.REJECTED.value.upper()
            )
            return True
        else:
            self.logger.info(
                "Application decision cannot be completed, pending security clearance or board decision."
            )
            return False

    def security_clearance(self):
        if not self._security_clearance:
            try:
                return SecurityClearance.objects.get(
                    document_number=self.document_number
                )
            except SecurityClearance.DoesNotExist:
                self.logger.info(
                    f"Security clearance is pending for {self.document_number}"
                )
        else:
            return self._security_clearance

    def board_decision(self):
        if not self._board_decision:
            try:
                return BoardDecision.objects.get(document_number=self.document_number)
            except BoardDecision.DoesNotExist:
                self.logger.info(
                    f"Board decision is pending for {self.document_number}"
                )
        else:
            return self._board_decision

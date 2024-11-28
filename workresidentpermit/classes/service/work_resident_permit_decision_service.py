import logging

from app.classes.mixins.update_application_mixin import UpdateApplicationMixin
from app.models import Application, SecurityClearance
from app.utils import ApplicationDecisionEnum
from app_comments.models import Comment
from app.service import ApplicationDecisionService
from board.models import BoardDecision

from app.workflow import ProductionTransactionData


class WorkResidentPermitDecisionService(
    ApplicationDecisionService, UpdateApplicationMixin
):
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
        self.workflow = ProductionTransactionData()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def update_application(self):
        # Update the application field with the decision status
        self.update_application_field(
            document_number=self.document_number,
            field_key="board",
            field_value=self.board_decision.decision_outcome.upper(),
        )
        print(
            f"*******************************{self.board_decision.decision_outcome.upper()}"
        )

    def decision_predicate(self):
        is_security_clearance_accepted = False
        is_board_decision_taken = False

        if self.security_clearance:
            is_security_clearance_accepted = (
                self.security_clearance.status.code.lower()
                == ApplicationDecisionEnum.ACCEPTED.value.lower()
            )
        if self.board_decision:
            is_board_decision_taken = (
                self.board_decision.decision_outcome.lower()
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
        elif self.board_decision and self.security_clearance:
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

    @property
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

    @property
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

    def is_allowed_create_dependent_application_decision(self) -> bool:
        return True

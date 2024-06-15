import logging

from django.db import transaction
from django.shortcuts import get_object_or_404

from app.models import Application, ApplicationStatus

from workflow.signals import create_or_update_task_signal
from workflow.classes import WorkflowTransition

from app_comments.models import Comment
from board.models import BoardDecision
from workresidentpermit.exceptions import WorkResidentPermitApplicationDecisionException
from workresidentpermit.models import SecurityClearance, CommissionerDecision
from app.utils import ApplicationDecisionEnum, ApplicationStatuses, WorkflowEnum

from workresidentpermit.workflow import ProductionTransactionData

from app_decision.models import ApplicationDecision, ApplicationDecisionType


class WorkResidentPermitApplicationDecisionService:
    """ Responsible for create application decision based on security clearance or board decision.
    """

    def __init__(self, document_number, security_clearance: SecurityClearance = None,
                 board_decision: BoardDecision = None,
                 comment: Comment = None, commissioner_decision: CommissionerDecision = None):
        self.document_number = document_number
        self._board_decision = board_decision
        self._security_clearance = security_clearance
        self._commissioner_decision = commissioner_decision
        self.comment = comment
        self.application = None
        self.logger = logging.getLogger(__name__)

    def commissioner_decision(self):
        if not self._commissioner_decision:
            try:
                self._commissioner_decision = CommissionerDecision.objects.get(
                    document_number=self.document_number
                )
            except CommissionerDecision.DoesNotExist:
                pass
        else:
            return self._commissioner_decision

    def security_clearance(self):
        if not self._security_clearance:
            try:
                return SecurityClearance.objects.get(
                    document_number=self.document_number
                )
            except SecurityClearance.DoesNotExist:
                self.logger.info(f"Security clearance is pending for {self.document_number}")
        else:
            return self._security_clearance

    def board_decision(self):
        if not self._board_decision:
            try:
                return BoardDecision.objects.get(
                    assessed_application__application_document__document_number=self.document_number
                )
            except BoardDecision.DoesNotExist:
                self.logger.info(f"Board decision is pending for {self.document_number}")
        else:
            return self._security_clearance

    def create(self):
        is_security_clearance_accepted = False
        is_board_decision_taken = False
        is_commissioner_decision = False

        workflow = ProductionTransactionData()

        security_clearance = self.security_clearance()
        if security_clearance:
            is_security_clearance_accepted = security_clearance.status.code.lower() \
                                             == ApplicationDecisionEnum.ACCEPTED.value.lower()
        board_decision = self.board_decision()
        if board_decision:
            self.application = self._board_decision.assessed_application
            is_board_decision_taken = \
                self._board_decision.decision_outcome.lower() == ApplicationDecisionEnum.APPROVED.value.lower()

        commissioner_decision = self.commissioner_decision()
        if commissioner_decision:
            is_commissioner_decision = commissioner_decision.status.code.lower() == \
                                       ApplicationDecisionEnum.ACCEPTED.value.lower()

        if is_security_clearance_accepted and is_board_decision_taken:
            decision_type = ApplicationDecisionEnum.ACCEPTED.value
            decision_status = "ACCEPTED"
            workflow.board_decision = decision_status
            workflow.security_clearance = decision_status
        elif self._board_decision and security_clearance:
            decision_type = ApplicationDecisionEnum.REJECTED.value
            decision_status = "REJECTED"
        elif is_commissioner_decision:
            decision_type = ApplicationDecisionEnum.ACCEPTED.value
            decision_status = "ACCEPTED"
        else:
            self.logger.info("Application decision cannot be completed, pending security clearance or board decision.")
            return

        proposed_application_decision = self.application_decision_type(decision_type)
        self.create_application_decision(proposed_application_decision)
        self.logger.info(f"Application decision has been created successfully with status: {decision_status}.")

    def application_decision_type(self, decision_value: str) -> ApplicationDecisionType:
        try:
            proposed_application_decision_type = get_object_or_404(
                ApplicationDecisionType, code__iexact=decision_value
            )
            return proposed_application_decision_type
        except ApplicationDecisionType.DoesNotExist:
            error_message = (
                f"Application decision type cannot be found using decision_type: {decision_value}"
            )
            self.logger.error(error_message)
            raise WorkResidentPermitApplicationDecisionException(error_message)

    @transaction.atomic()
    def create_application_decision(self, proposed_decision: ApplicationDecisionType):
        ApplicationDecision.objects.create(
            final_decision_type=None,
            proposed_decision_type=proposed_decision,
            comment=self.comment
        )
        self.run_workflow(application=self._board_decision.assessed_application)

    def run_workflow(self, application: Application):
        """
        TODO: Refactor as per the new workflow changes..
        :param application:
        :return:
        """
        self.logger.info(f"START the workflow for {application.application_document.document_number}")
        previous_activity = application.application_status.code.upper()
        source_data = WorkflowTransition(
            previous_status=previous_activity
        )
        application_status = ApplicationStatus.objects.get(code__iexact=ApplicationStatuses.ACCEPTED.value)
        application.application_status = application_status
        application.save()
        source_data.current_status = WorkflowEnum.FINAL_DECISION.value
        source_data.next_activity_name = WorkflowEnum.PERMIT_CANCELLATION.value
        create_or_update_task_signal.send_robust(sender=application, source=source_data, application=application)
        self.logger.info(f"END the workflow for {application.application_document.document_number}")

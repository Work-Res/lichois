import logging
from abc import abstractmethod

from django.db import transaction
from django.shortcuts import get_object_or_404

from app.models import Application
from app_comments.models import Comment
from app_decision.models import ApplicationDecision, ApplicationDecisionType
from workflow.signals import create_or_update_task_signal
from workresidentpermit.exceptions import (
    ApplicationRequiredDecisionException,
    WorkflowRequiredDecisionException,
    WorkResidentPermitApplicationDecisionException,
)
from workresidentpermit.workflow import BaseTransactionData


class ApplicationDecisionService:
    """Responsible for create application decision based on security clearance or board decision."""

    def __init__(self, document_number, comment: Comment = None):
        self.document_number = document_number
        self.comment = comment
        self.decision_value = None
        self.application = None
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def decision_predicate(self):
        """
        Evaluate required business rules for production, and returns True or False for creating application decision.
        Please override this method on based class for decision making
        :return: True or False.
        """
        print("Running running running..")
        return False

    def proposed_application_decision_type(self) -> ApplicationDecisionType:
        try:
            proposed_application_decision_type = get_object_or_404(
                ApplicationDecisionType, code__iexact=self.decision_value
            )
            return proposed_application_decision_type
        except ApplicationDecisionType.DoesNotExist:
            error_message = f"Application decision type cannot be found using decision_type: {self.decision_value}"
            self.logger.error(error_message)
            raise WorkResidentPermitApplicationDecisionException(error_message)

    @transaction.atomic()
    def create_application_decision(self):
        if not self.application:
            raise ApplicationRequiredDecisionException()
        if not self.workflow:
            raise WorkflowRequiredDecisionException()
        if self.decision_predicate():
            ApplicationDecision.objects.create(
                document_number=self.document_number,
                final_decision_type=None,
                proposed_decision_type=self.proposed_application_decision_type(),
                comment=self.comment,
            )
            self.run_workflow(application=self.application, workflow=self.workflow)

    def run_workflow(self, application: Application, workflow: BaseTransactionData):
        """
        TODO: Refactor as per the new workflow changes..
        :param application:
        :param workflow:
        :return:
        """
        self.logger.info(
            f"START the workflow for {application.application_document.document_number}"
        )
        create_or_update_task_signal.send_robust(
            sender=application, source=workflow, application=application
        )
        self.logger.info(
            f"END the workflow for {application.application_document.document_number}"
        )

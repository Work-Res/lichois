import logging

from django.db import transaction

from app.api.common.web import APIMessage, APIResponse
from app.api.serializers import ApplicationSerializer
from app.models import Application, ApplicationStatus, ApplicationVerification
from app.utils import ApplicationStatusEnum
from app_comments.models import Comment
from app.models import ApplicationDecisionType
from workflow.classes import TaskDeActivation
from workflow.signals import create_or_update_task_signal
from workresidentpermit.workflow import (
    VerificationTransactionData,
    VettingTransactionData,
)


class WorkResidentPermitApplication:
    """
    Responsible for

    1. trigger workflow model for task creation via signal
    2. send an acknowledgement.
    3. Update application status
    """

    def __init__(self, document_number, verification_request=None, user=None):
        self.verification_request = verification_request
        self.user = user
        self.response = APIResponse()

        self.logger = logging.getLogger(__name__)
        self.document_number = document_number
        self.application = Application.objects.get(
            application_document__document_number=document_number
        )

    def submit_verification(self):
        """
        1. CRM Acknowledgement via Communication platform
        2. Generate consolidated document including attached documents
        3. Changed application status to PENDING_BOARD or PENDING_SECURITY_CLEARANCE. (
        Trigger workflow tasks creations )
        4. Close verification task( TODO: Confirm current task closure )
        """
        self.logger.info(f"Verification process started. {self.document_number}")
        # WorkPermitApplicationPDFGenerator TODO: Review business needs
        with transaction.atomic():
            workflow = VettingTransactionData()
            # Fixme add condition to check if comment is provided
            comment = None
            if self.verification_request.comment:
                comment = Comment.objects.create(
                    user=self.user,
                    comment_text=self.verification_request.comment,
                    comment_type="OVERALL_APPLICATION_COMMENT",
                )
            application_decision_type = ApplicationDecisionType.objects.get(
                code__iexact=self.verification_request.decision.lower()
            )

            workflow.verification_decision = application_decision_type.code.upper()
            workflow.current_status = self.application.application_status.code
            self.application.verification = application_decision_type.code
            self.application.save()

            ApplicationVerification.objects.create(
                document_number=self.document_number,
                comment=comment,
                decision=application_decision_type,
                outcome_reason=self.verification_request.outcome_reason,
            )

            self.logger.info("Application has been submitted successfully.")
            self.response.messages.append(
                APIMessage(
                    code=200,
                    message="Application verification submission",
                    details="Application has been submitted successfully.",
                ).to_dict()
            )
            self.response.data = ApplicationSerializer(self.application).data
            # input decision
            create_or_update_task_signal.send(
                self.application, source=workflow, application=self.application
            )

            self.logger.info(f"Verification process ended. {self.document_number}")
            task_deactivation = TaskDeActivation(
                application=self.application, source=None, model=None
            )
            task_deactivation.update_task_by_activity(
                name=ApplicationStatusEnum.VERIFICATION.value
            )
            return self.response

    def submit(self):
        self.logger.info("Work resident submission process started.")
        workflow = VerificationTransactionData()
        workflow.system_verification = "validated"
        with transaction.atomic():
            self.logger.info("Application has been submitted successfully.")
            application_status = ApplicationStatus.objects.get(
                code__iexact=ApplicationStatusEnum.DRAFT.value
            )
            self.application.application_status = application_status
            self.application.save()

            self.response.messages.append(
                APIMessage(
                    code=200,
                    message="Application submission",
                    details="Application has been submitted successfully.",
                ).to_dict()
            )
            self.response.data = ApplicationSerializer(self.application).data
            self.logger.info("Work resident submission process ended.")

            create_or_update_task_signal.send_robust(
                sender=self.application, source=workflow, application=self.application
            )
            self.logger.debug("Task event signal completed")
            return self.response

    def cancel(self):
        pass

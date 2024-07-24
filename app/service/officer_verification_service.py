import logging

from app.api.dto.application_verification_request_dto import (
    ApplicationVerificationRequestDTO,
)
from app.models import Application, ApplicationVerification
from app.workflow import OfficerTransactionData
from app_comments.models import Comment

from app.utils import ApplicationStatusEnum
from app.api.common.web import APIResponse, APIMessage
from app.api.serializers import ApplicationSerializer

from app_decision.models import ApplicationDecisionType

from workflow.signals import create_or_update_task_signal
from workflow.classes import TaskDeActivation


from django.db import transaction


class OfficerVerificationService:
    """Responsible for updating the application, after the officer verifies content of the application."""

    def __init__(
        self,
        document_number,
        verification_request: ApplicationVerificationRequestDTO,
        user=None,
    ):
        self.verification_request = verification_request
        self.user = user
        self.response = APIResponse()

        self.logger = logging.getLogger(__name__)
        self.document_number = document_number
        self.application = Application.objects.get(
            application_document__document_number=document_number
        )

    def submit(self):
        """ """
        self.logger.info(f"Verification submission started. {self.document_number}")
        with transaction.atomic():
            workflow = OfficerTransactionData()
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

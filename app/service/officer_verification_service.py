import logging
from django.db import transaction

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
        self.application = self._get_application(document_number)

    def _get_application(self, document_number):
        return Application.objects.get(
            application_document__document_number=document_number
        )

    def _create_comment(self):
        if self.verification_request.comment:
            return Comment.objects.create(
                user=self.user,
                comment_text=self.verification_request.comment,
                comment_type="OVERALL_APPLICATION_COMMENT",
            )
        return None

    def _get_application_decision_type(self):
        return ApplicationDecisionType.objects.get(
            code__iexact=self.verification_request.decision.lower()
        )

    def _update_application(self, application_decision_type):
        self.application.verification = application_decision_type.code
        self.application.save()

    def _create_application_verification(self, comment, application_decision_type):
        ApplicationVerification.objects.create(
            document_number=self.document_number,
            comment=comment,
            decision=application_decision_type,
            outcome_reason=self.verification_request.outcome_reason,
        )

    def _send_task_signal(self, workflow):
        create_or_update_task_signal.send(
            self.application, source=workflow, application=self.application
        )

    def _deactivate_task(self):
        task_deactivation = TaskDeActivation(
            application=self.application, source=None, model=None
        )
        task_deactivation.update_task_by_activity(
            name=ApplicationStatusEnum.VERIFICATION.value
        )

    def _log_info(self, message):
        self.logger.info(f"{message} {self.document_number}")

    def _add_response_message(self, code, message, details):
        self.response.messages.append(
            APIMessage(
                code=code,
                message=message,
                details=details,
            ).to_dict()
        )

    def _set_response_data(self):
        self.response.data = ApplicationSerializer(self.application).data

    def submit(self):
        self._log_info("Verification submission started.")
        with transaction.atomic():
            workflow = OfficerTransactionData()
            comment = self._create_comment()
            application_decision_type = self._get_application_decision_type()

            workflow.verification_decision = application_decision_type.code.upper()
            workflow.current_status = self.application.application_status.code

            self._update_application(application_decision_type)
            self._create_application_verification(comment, application_decision_type)

            self._log_info("Application has been submitted successfully.")
            self._add_response_message(
                code=200,
                message="Application verification submission",
                details="Application has been submitted successfully.",
            )
            self._set_response_data()

            self._send_task_signal(workflow)
            self._deactivate_task()

            self._log_info("Verification process ended.")
            return self.response

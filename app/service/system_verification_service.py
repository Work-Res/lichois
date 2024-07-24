import logging

from app.api.dto.application_verification_request_dto import (
    ApplicationVerificationRequestDTO,
)
from app.models import Application, ApplicationStatus

from app.utils import ApplicationStatusEnum, VerificationStatusEnum
from app.api.common.web import APIResponse, APIMessage
from app.api.serializers import ApplicationSerializer
from app.workflow import VerificationTransactionData

from workflow.signals import create_or_update_task_signal


from django.db import transaction


class SystemVerificationService:
    """Responsible for updating the application after successfully validationg the CRM application, and receiving it in
    the system.
    """

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
        self.logger.info("System verification submission")
        workflow = VerificationTransactionData()
        workflow.system_verification = VerificationStatusEnum.VALIDATED.value.lower()
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

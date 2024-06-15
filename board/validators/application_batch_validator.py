from ..classes.dto import ApplicationBatchRequestDTO
from app.models import Application
from app.api.common.web import APIMessage, APIResponse
from ..models import ApplicationBatch

from app.utils import ApplicationStatusEnum


class ApplicationBatchValidator:

    def __init__(self, application_batch_request: ApplicationBatchRequestDTO):
        self.application_batch_request = application_batch_request
        self.response = APIResponse()

    def add_error_message(self, detail, document_number):
        api_message = APIMessage(
            code=400,
            message="Bad request",
            details=f"{detail}, {document_number}."
        )
        self.response.messages.append(api_message.to_dict())

    def is_invalid_application(self, application):
        return self.check_application_status(application) or self.check_application_in_batch(application)

    def validate_batches(self):
        applications = Application.objects.filter(id__in=self.application_batch_request.applications)
        eligible_applications = [
            application for application in applications
            if not self.is_invalid_application(application)
        ]

        if not eligible_applications:
            # Assuming you want to add an error message for all invalid applications
            for application in applications:
                self.add_error_message(
                    "The system cannot create an empty application batch.",
                    application.application_document.document_number
                )

    def is_valid(self):
        self.validate_batches()
        success = not self.response.messages
        if success:
            self.response.status = "success"
        else:
            self.response.status = "failed"
        return not self.response.messages

    def check_application_status(self, application: Application):
        error = False
        if application.application_status.code.lower() != ApplicationStatusEnum.VETTING.value.lower():
            self.add_error_message(
                "Only applications at the vetting stage can be added to a batch",
                application.application_document.document_number
            )
            error = True
        return error

    def check_application_in_batch(self, application: Application):
        error = False
        if ApplicationBatch.objects.filter(applications__id=application.id).exists():
            self.add_error_message(
                "Application already added in another batch",
                application.application_document.document_number
            )
            error = True
        return error

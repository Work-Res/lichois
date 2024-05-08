import logging

from datetime import date

from app.models import Application, ApplicationStatus

from app.utils import ApplicationStatuses
from app.api.common.web import APIResponse, APIError

from django.db import transaction


class WorkResidentPermitApplication:
    """
    Responsible for

    1. trigger workflow model for task creation via signal
    2. send an acknowledgement.
    3. Update application status
    """
    def __init__(self, document_number):
        self.response = APIResponse()
        self.logger = logging.getLogger(__name__)
        self.document_number = document_number
        self.application = Application.objects.get(application_document__document_number=document_number)

    def submit(self):
        with transaction.atomic():
            application_status = ApplicationStatus.objects.get(code=ApplicationStatuses.VERIFICATION.value)
            self.application.application_status = application_status
            self.application.submission_date = date.today()
            self.save()
            self.logger.info("Application has been submitted successfully.")
            self.response.messages.append(
                APIError(
                    code=200,
                    message="Application submission",
                    details=f"Application has been submitted successfully.")
            )
            self.response.data = self.application
            return self.response

    def cancel(self):
        pass


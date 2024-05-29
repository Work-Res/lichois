import logging

from typing import Optional

from app.models import Application
from app.api.common.web import APIResponse, APIMessage
from app.utils import ApplicationStatuses


class SecurityClearanceValidator:

    def __init__(self, document_number: Optional[str] = None):
        """
        Initialize the SecurityClearanceValidator with an optional document number.
        """
        self.logger = logging.getLogger(__name__)
        self.document_number = document_number
        self.response = APIResponse()
        self.application = None

        if document_number:
            self._fetch_application()

    def _fetch_application(self):
        """
        Fetch the application with the given document number and vetting status.
        """
        try:
            self.application = Application.objects.get(
                application_document__document_number=self.document_number,
                application_status__code=ApplicationStatuses.VETTING.value
            )
        except Application.DoesNotExist:
            self.logger.error(f"Application with document number {self.document_number} does not exist or is not in vetting status.")
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Incorrect Application Status for Clearance",
                    details="An application cannot be security cleared if not at VETTING stage."
                ).to_dict()
            )
        except Exception as e:
            self.logger.exception(f"An unexpected error occurred while fetching the application: {e}")
            self.response.messages.append(
                APIMessage(
                    code=500,
                    message="Internal Server Error",
                    details="An unexpected error occurred. Please try again later."
                ).to_dict()
            )

    def is_valid(self) -> bool:
        """
        Check if the validator has no error messages, implying the application is valid for clearance.
        Returns:
            bool: True if there are no error messages, False otherwise.
        """
        return not self.response.messages

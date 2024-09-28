import logging
from typing import Optional


from ..api.common.web import APIMessage, APIResponse
from ..models import Application, SecurityClearance, ApplicationDecisionType
from ..utils import ApplicationStatusEnum


class SecurityClearanceValidator:

    def __init__(self, document_number: Optional[str] = None, status=None):
        """
        Initialize the SecurityClearanceValidator with an optional document number.
        """
        self.logger = logging.getLogger(__name__)
        self.document_number = document_number
        self.response = APIResponse()
        self.application = None
        self.status = status

        if document_number:
            self._fetch_application()

    def _fetch_application(self):
        """
        Fetch the application with the given document number and vetting status.
        """
        try:
            self.application = Application.objects.get(
                application_document__document_number=self.document_number,
                application_status__code__iexact=ApplicationStatusEnum.VETTING.value,
            )
        except Application.DoesNotExist:
            self.logger.error(
                f"Application with document number {self.document_number} does not exist or is not in vetting status."
            )
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Incorrect Application Status for Clearance",
                    details="An application cannot be security cleared if not at VETTING stage.",
                ).to_dict()
            )
        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred while fetching the application: {e}"
            )
            self.response.messages.append(
                APIMessage(
                    code=500,
                    message="Internal Server Error",
                    details="An unexpected error occurred. Please try again later.",
                ).to_dict()
            )

    def check_security_clearance_exists(self):

        try:
            SecurityClearance.objects.get(document_number=self.document_number)
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Security Clearance already exists.",
                    details="Security clearance has been completed already.",
                ).to_dict()
            )
        except SecurityClearance.DoesNotExist:
            pass
        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred while validating security clearance: {e}"
            )
            self.response.messages.append(
                APIMessage(
                    code=500,
                    message="Internal Server Error",
                    details=f"An unexpected error occurred. Please try again later. Got {e}",
                ).to_dict()
            )

    def check_application_decision_type(self):
        try:
            ApplicationDecisionType.objects.get(code__iexact=self.status)
        except ApplicationDecisionType.DoesNotExist:
            print("Security decision not found.")
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Invalid status",
                    details="Kindly provide a valid status, pending, accepted or rejected.",
                ).to_dict()
            )

    def is_valid(self) -> bool:
        """
        Check if the validator has no error messages, implying the application is valid for clearance.
        Returns:
            bool: True if there are no error messages, False otherwise.
        """
        self.check_security_clearance_exists()
        self.check_application_decision_type()
        return not self.response.messages

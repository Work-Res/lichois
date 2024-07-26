import logging
from app.api.common.web import APIMessage, APIResponse
from app.models import Application
from app_address.models import ApplicationAddress
from app_attachments.models import ApplicationAttachment
from app_checklist.models import ChecklistClassifierItem
from app_personal_details.models import Person
from ..models import TravelCertificate, ApplicantRelative

class TravelCertificateValidator:
    """
    Validates mandatory fields and attachments for a travel certificate application.
    """

    def __init__(
        self,
        process=None,
        travel_certificate: TravelCertificate = None,
        document_number=None,
        application_type=None,
    ):
        self.logger = logging.getLogger(__name__)
        self.document_number = document_number if document_number else ""
        self.process = process
        self.application_type = application_type
        self.response = APIResponse()
        try:
            self.application = Application.objects.get(
                application_document__document_number=document_number
            )
            self.travel_certificate = travel_certificate
        except Application.DoesNotExist:
            self.add_error(
                code=400,
                message="Incorrect document number",
                details=f"An application with document number {document_number} was not found."
            )

    def validate(self):
        """
        Perform validation by checking mandatory fields and attachments.
        """
        self.validate_mandatory_attachments()
        self.find_missing_mandatory_fields()

    def is_valid(self):
        """
        Returns True or False based on the validation results.
        """
        self.validate()
        return len(self.response.messages) == 0

    def add_error(self, code, message, details):
        """
        Adds an error message to the response.
        """
        self.response.messages.append(
            APIMessage(
                code=code,
                message=message,
                details=details
            ).to_dict()
        )

    def find_missing_mandatory_fields(self):
        """
        Check if all required models are captured.
        """
        models_to_check = {
            Person: "Personal details are missing. Please submit the form.",
            ApplicationAddress: "Address details are mandatory. Please submit the form.",
            TravelCertificate: "Travel certificate details are missing. Please submit the form.",
            ApplicantRelative: "Applicant relative details are missing."
        }

        for model, message in models_to_check.items():
            if not model.objects.filter(document_number=self.document_number).exists():
                self.add_error(
                    code=400,
                    message="Required Data",
                    details=message
                )

    def validate_mandatory_attachments(self):
        """
        Check if all required attachments for a business process are captured.
        """
        self.logger.info(f"Processing attachments for process: {self.process}")
        attachments = ChecklistClassifierItem.objects.filter(
            checklist_classifier__code="ATTACHMENT_DOCUMENTS",
            checklist_classifier__process_name__icontains=self.process if self.process else "",
            mandatory=True,
            application_type=self.application_type,
        )
        attached_codes = set(
            ApplicationAttachment.objects.filter(
                document_number=self.document_number
            ).values_list("document_type__code", flat=True)
        )
        missing_attachments = attachments.exclude(code__in=attached_codes)

        for attachment in missing_attachments:
            self.add_error(
                code=400,
                message="Attachments are required.",
                details=f"A mandatory attachment is required: {attachment.name}"
            )

    def validate_payment(self):
        """
        Check if the payment is created before a work resident permit application can be submitted.
        """
        pass

    def validate_declaration_of_truth(self):
        """
        Validate the declaration of truth.
        """
        pass

    def validate_cancellation(self):
        """
        Check if the application is valid to be cancelled.
        """
        pass

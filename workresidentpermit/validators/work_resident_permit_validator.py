import logging

from app_checklist.models import ClassifierItem
from app_attachments.models import ApplicationAttachment
from app_personal_details.models import Person, Passport, Permit
from app_contact.models import ApplicationContact
from app.models import Application
from app.api.common.web import APIResponse, APIError


class WorkResidentPermitValidator:

    """
    Responsible for validating all mandatory for work resident and permit.
    """

    def __init__(self, process=None, work_resident_permit=None, document_number=None):
        self.logger = logging.getLogger(__name__)
        try:
            self.application = Application.objects.get(
                application_document__document_number=document_number)
            self.process = process
            self.work_resident_permit = work_resident_permit
            self.document_number = document_number
            self.response = APIResponse()
        except Application.DoesNotExist:
            self.response.messages.append(
                APIError(
                    code=400,
                    message="Incorrect document number",
                    details=f"An application with {document_number} is not found. "
                )
            )

    def validate(self):
        self.validate_mandatory_attachments()
        self.find_missing_mandatory_fields()
        self.validate_contacts()
        self.validate_preferred_channels()

    def is_valid(self):
        """
        Returns True or False after running the validate method.
        """
        self.validate()
        return True if len(self.response.messages) == 0 else False

    def find_missing_mandatory_fields(self):
        """
        Check if all required models are captured.
        """
        try:
            Person.objects.get(document_number=self.document_number)
        except Person.DoesNotExist:
            self.response.messages.append(
                APIError(
                    code=400,
                    message="Required Data",
                    details=f"A personal details are missing, kindly submit the form. "
                )
            )

        try:
            Passport.objects.get(document_number=self.document_number)
        except Passport.DoesNotExist:
            self.response.messages.append(
                APIError(
                    code=400,
                    message="Required Data",
                    details=f"A passport details are missing, kindly submit the form. "
                )
            )

        try:
            Permit.objects.get(document_number=self.document_number)
        except Permit.DoesNotExist:
            self.response.messages.append(
                APIError(
                    code=400,
                    message="Required Data",
                    details=f"A permit details are missing, kindly submit the form. "
                )
            )

        contacts_count = ApplicationContact.objects.filter(document_number=self.document_number).count()
        if contacts_count == 0:
            self.response.messages.append(
                APIError(
                    code=400,
                    message="Required Field",
                    details="Application contacts are missing. Please submit the required information."
                )
            )

    def validate_mandatory_attachments(self):
        """
        Check if all required attachments for a business process are captured.
        """
        attachments = ClassifierItem.objects.filter(
            classifier__code="ATTACHMENT_DOCUMENTS",
            process__icontains=self.process,
            mandatory=True
        )
        attached_codes = set(
            ApplicationAttachment.objects.filter(document_number=self.document_number).values_list('code', flat=True))
        missing_attachments = attachments.exclude(code__in=attached_codes)

        for attachment in missing_attachments:
            self.response.messages.append(
                APIError(
                    code=400,
                    message="Required Field",
                    details=f"A mandatory attachment is required: {attachment.name}"
                )
            )

    def validate_payment(self):
        """
        Check if the payment is created before an work resident permit application can be submited.
        """
        pass
    
    def validate_preferred_channels(self):
        contacts_count = ApplicationContact.objects.filter(
            document_number=self.document_number, preferred_method_comm=True).count()
        if contacts_count == 0:
            self.response.messages.append(
                APIError(
                    code=400,
                    message="Required Field",
                    details=f"Kindly indicate preferred channel of communication, e.g EMAIL or PHONE."
                )
            )

    def validate_declaration_of_truth(self):
        pass

    def validate_cancellation(self):
        """
        Check if the application is valid to be cancelled.
        """
        pass

import logging

from app_checklist.models import ClassifierItem
from app_attachments.models import ApplicationAttachment
from app_personal_details.models import Person, Passport
from app_contact.models import ApplicationContact
from app_address.models import ApplicationAddress
from app.models import Application
from app.api.common.web import APIResponse, APIMessage
from workresidentpermit.models import WorkPermit


class WorkResidentPermitValidator:
    """
    Responsible for validating all mandatory for work resident and permit.
    """

    def __init__(self, process=None, work_resident_permit=None, document_number=None):
        self.logger = logging.getLogger(__name__)
        self.document_number = document_number if document_number else ""
        self.process = process
        self.response = APIResponse()
        try:
            self.application = Application.objects.get(
                application_document__document_number=document_number)
            self.work_resident_permit = work_resident_permit
        except Application.DoesNotExist:
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Incorrect document number",
                    details=f"An application with {document_number} is not found. "
                ).to_dict()
            )

    def validate(self):
        self.validate_mandatory_attachments()
        self.find_missing_mandatory_fields()
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
                APIMessage(
                    code=400,
                    message="Required Data",
                    details=f"A personal details are missing, kindly submit the form. "
                ).to_dict()
            )

        try:
            Passport.objects.get(document_number=self.document_number)
        except Passport.DoesNotExist:
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Passport are a mandatory.",
                    details=f"A passport details are missing, kindly submit the form. "
                ).to_dict()
            )

        try:
            ApplicationAddress.objects.get(document_number=self.document_number)
        except ApplicationAddress.DoesNotExist:
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Address are a mandatory.",
                    details=f"A permit details are missing, kindly submit the form. "
                ).to_dict()
            )

        contacts_count = ApplicationContact.objects.filter(document_number=self.document_number).count()
        if contacts_count == 0:
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Address contacts are a mandatory.",
                    details="Application contacts are missing. Please submit the required information."
                ).to_dict()
            )

    def validate_mandatory_attachments(self):
        """
        Check if all required attachments for a business process are captured.
        """
        print("self.process ", self.process)
        attachments = ClassifierItem.objects.filter(
            classifier__code="ATTACHMENT_DOCUMENTS",
            process__icontains=self.process if self.process else "",
            mandatory=True
        )
        attached_codes = set(
            ApplicationAttachment.objects.filter(document_number=self.document_number).values_list(
                'document_type__code', flat=True))
        missing_attachments = attachments.exclude(code__in=attached_codes)

        for attachment in missing_attachments:
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Attachments are required.",
                    details=f"A mandatory attachment is required: {attachment.name}"
                ).to_dict()
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
                APIMessage(
                    code=400,
                    message="Required Field",
                    details=f"Kindly indicate preferred channel of communication, e.g EMAIL or PHONE."
                ).to_dict()
            )

    def validate_declaration_of_truth(self):
        pass

    def validate_cancellation(self):
        """
        Check if the application is valid to be cancelled.
        """
        pass

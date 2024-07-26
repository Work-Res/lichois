import logging
from app.api.common.web import APIMessage, APIResponse
from app.models import Application
from app_address.models import ApplicationAddress
from app_attachments.models import ApplicationAttachment
from app_checklist.models import ChecklistClassifierItem
from app_personal_details.models import Person, Passport, NextOfKin
from app_contact.models import ApplicationContact
from ..models import BlueCard

class BlueCardValidator:
    def __init__(
            self,
            process=None,
            blue_card_application=BlueCard,
            document_number=None,
            application_type=None
    ):
        self.logger = logging.getLogger(__name__)
        self.document_number = document_number if document_number else ""
        self.process = process
        self.application_type = application_type
        self.response = APIResponse()
        self.response.messages = []
        try:
            self.application = Application.objects.get(
                application_document__document_number=document_number
            )
            self.blue_card_application = blue_card_application
        except Application.DoesNotExist:
            self.add_error(
                code=400,
                message="Incorrect document number",
                details=f"An application with document number {document_number} was not found."
            )

    def validate(self):
        self.validate_mandatory_attachments()
        self.find_missing_mandatory_fields()
        self.validate_preferred_channels()

    def is_valid(self):
        self.validate()
        return len(self.response.messages) == 0
    
    def add_error(self, code, message, details):
        self.response.messages.append(
            APIMessage(
                code=code,
                message=message,
                details=details
            ).to_dict()
        )

    def find_missing_mandatory_fields(self):
        models_to_check = {
            Person: "Personal details are missing. Please submit the form.",
            ApplicationAddress: "Address details are mandatory. Please submit the form.",
            Passport:"Passport details are missing.",
            ApplicationContact:"Preferred method of contact is missing.",
            NextOfKin:"Next of kin details are mandatory."
        }

        for model, message in models_to_check.items():
            if not model.objects.filter(document_number=self.document_number).exists():
                self.add_error(
                    code=400,
                    message="Required Data",
                    details=message
                )

    def validate_mandatory_attachments(self):
        
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

    def validate_preferred_channels(self):
        contacts_count = ApplicationContact.objects.filter(
            document_number=self.document_number, preferred_method_comm=True
        ).count()
        if contacts_count == 0:
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Required Field",
                    details="Kindly indicate preferred channel of communication, e.g EMAIL or PHONE.",
                ).to_dict()
            )

    def validate_payment(self):
        pass

    def validate_declaration_of_truth(self):
        pass

    def validate_cancellation(self):
        pass
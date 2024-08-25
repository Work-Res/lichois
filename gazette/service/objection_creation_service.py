import re
import logging
from django.core.exceptions import ObjectDoesNotExist
from django_mailbox.models import Message
from app.models import Application
from ..models.objection import Objection

# Set up logging
logger = logging.getLogger(__name__)


class ObjectionCreationService:

    def __init__(self, name=None):
        self.document_number_pattern = (
            r"\b[A-Z0-9]{8,12}\b"  # Example regex to match document numbers
        )
        self.name = name

    def process_incoming_emails(self):
        """
        Fetches unread emails, searches for document numbers in the subject, and creates objections
        """
        messages = Message.objects.filter(
            processed__isnull=False, mailbox__name=self.name
        )

        for message in messages:
            document_number = self.extract_document_number(message.subject)
            if document_number:
                self.create_objection_if_applicable(document_number, message)
                message.mailbox.mark_as_seen(message)  # Mark email as read

    def extract_document_number(self, subject):
        """
        Extracts the document number from the email subject using a regex pattern
        """
        match = re.search(self.document_number_pattern, subject)
        if match:
            return match.group(0)
        return None

    def create_objection_if_applicable(self, document_number, message):
        """
        Looks up the application by document number and creates an objection if a match is found
        """
        try:
            application = Application.objects.get(document_number=document_number)

            # Check if an objection already exists for this application from this email
            if not Objection.objects.filter(
                application=application, email=message.from_address
            ).exists():
                objection = Objection.objects.create(
                    application=application,
                    name=message.from_address,
                    email=message.from_address,
                    message=message.text or message.html,
                    attachment=(
                        message.attachments.first()
                        if message.attachments.exists()
                        else None
                    ),
                )
                logger.info(
                    f"Objection created for application {application.application_document.document_number} based on "
                    f"email from {message.from_address}"
                )
            else:
                logger.info(
                    f"Objection already exists for application {application.application_document.document_number} from {message.from_address}"
                )
        except ObjectDoesNotExist:
            logger.warning(
                f"No matching application found for document number: {document_number}"
            )

import logging

from app.api.common.web import APIResponse, APIMessage
from django.db import IntegrityError, DatabaseError, transaction

from app_attachments.models import ApplicationAttachment, AttachmentDocumentType
from app.models import ApplicationVersion


class CreateNewApplicationAttachment(object):
    """Create New Application Attachment.
    """

    def __init__(self, data={}):
        self.data = data
        self.document_number = None
        self.logger = logging.getLogger(__name__)
        self.response = APIResponse()

    def application_version(self):
        try:
            application_version = ApplicationVersion.objects.get(
                application__application_document__document_number=self.document_number)
            return application_version
        except ApplicationVersion.DoesNotExist:
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details=f"An application document does not exists with: {self.document_number}"
            )
            self.response.status = False
            self.response.messages.append(api_message.to_dict())

    @transaction.atomic()
    def create_attachment_type(self, attachment_type: dict):

        try:
            return AttachmentDocumentType.objects.create(**attachment_type)
        except IntegrityError as e:
            logging.error(f"Integrity error while creating attachment type: {e}")
            raise
        except DatabaseError as e:
            logging.error(f"Database error while creating attachment type: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while creating attachment type: {e}")
            raise

    @transaction.atomic()
    def create(self):
        """
         Create new application attachment record
        """
        try:
            application_version = self.application_version()
            if application_version:
                self.data['application_version'] = application_version
                attachment_type = self.data.get('document_type')
                self.data['document_type'] = self.create_attachment_type(attachment_type)
                ApplicationAttachment.objects.create(**self.data)
                self.response.status = "success"
                api_message = APIMessage(
                    code=200,
                    message="Success",
                    details="The system created application attachment details successfully."
                )
                self.response.status = True
                self.response.messages.append(api_message.to_dict())
        except Exception as e:
            self.logger.debug(f"Something went wrong. The system failed to create application attachment details, {e}")
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details=f"Something went wrong. The system failed to create application attachment details.{e}"
            )
            self.response.status = False
            self.response.messages.append(api_message.to_dict())

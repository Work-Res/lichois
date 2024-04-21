import logging

from app.api.common.web import APIResponse, APIError

from app_attachments.models import ApplicationAttachment
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
            api_message = APIError(
                code=400,
                message="Bad request",
                details=f"An application document does not exists with: {self.document_number}"
            )
            self.response.status = False
            self.response.messages.append(api_message.to_dict())

    def create(self):
        """
         Create new application attachment record
        """
        try:
            application_version = self.application_version()
            if application_version:
                self.data['application_version'] = application_version

                ApplicationAttachment.objects.create(**self.data)
                self.response.status = True
                api_message = APIError(
                    code=200,
                    message="Success",
                    details="The system created application attachment details successfully."
                )
                self.response.status = True
                self.response.messages.append(api_message.to_dict())
        except Exception as e:
            self.logger.debug(f"The system failed to create application attachment details, something went wrong. {e}")
            api_message = APIError(
                code=400,
                message="Bad request",
                details=f"The system failed to create application attachment details, something went wrong.{e}"
            )
            self.response.status = False
            self.response.messages.append(api_message.to_dict())

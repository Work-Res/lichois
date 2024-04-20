import logging

from app.api.common.web import APIResponse, APIError

from app_personal_details.models import Person
from app.models import ApplicationVersion

from django.db import IntegrityError


class CreateNewPersonalDetails(object):
    """Responsible for creating new application records based on given process name.

        Attributes:
            new_application (ApplicationUser): user applying for visa or resident permit e.t.c
    """

    def __init__(self, data={}):
        self.data = data
        self.logger = logging.getLogger(__name__)
        self.response = APIResponse()

    def application_version(self):
        try:
            document_number = self.data.get("document_number")
            application_version = ApplicationVersion.objects.get(
                application__application_document__document_number=self.data.get("document_number"))
            return application_version
        except ApplicationVersion.DoesNotExist:
            api_message = APIError(
                code=400,
                message="Bad request",
                details=f"An application document does not exists with: {document_number}"
            )
            self.response.status = False
            self.response.messages.append(api_message.to_dict())

    def create(self):
        """
         Create new personal details
        """
        try:
            application_version = self.application_version()
            if application_version:
                self.data['application_version'] = application_version
                document_number = self.data['document_number']
                del self.data['document_number']
                Person.objects.create(**self.data)
                self.response.status = True
                api_message = APIError(
                    code=200,
                    message="Success",
                    details="The system created personal details successfully."
                )
                self.response.status = True
                self.response.messages.append(api_message.to_dict())
        except IntegrityError as e:
            self.logger.debug(
                f"The system cannot create multiple personal details for document number {document_number}. {e}")
            api_message = APIError(
                code=400,
                message="Bad request",
                details=f"The system cannot create multiple personal details for document number. {document_number}.{e}"
            )
            self.response.status = False
            self.response.messages.append(api_message.to_dict())
        except Exception as e:
            self.logger.debug(f"The system failed to create personal details, something went wrong. {e}")
            api_message = APIError(
                code=400,
                message="Bad request",
                details=f"The system failed to create personal details, something went wrong.{e}"
            )
            self.response.status = False
            self.response.messages.append(api_message.to_dict())

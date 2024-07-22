import logging

from app.api.common.web import APIMessage, APIResponse

from app.utils import ApplicationProcesses

from citizenship.utils import CitizenshipProcessEnum
from citizenship.identifier_config import RenunciationIdentifier


class CitizenshipDocumentGenerator:
    def __init__(self, application):
        self.application = application
        self.response = APIResponse()
        self.logger = logging.getLogger(__name__)

    def generate_document(self):
        """
        Generate document based on the given process.
        """
        process_name = self.application.proces_name

        # Get the appropriate identifier
        identifier = self.get_identifier(process_name)
        # self.stdout.write(self.style.SUCCESS(f"Identifier: {identifier}"))
        if identifier:
            return identifier

        # Handle special permits
        if process_name == ApplicationProcesses.SPECIAL_PERMIT.value:
            return self.get_special_permit_identifier()

        # Log an error if no valid process found
        self.log_invalid_process_error(process_name)
        return None

    def get_identifier(self, process_name):
        """
        Get the identifier for standard processes based on the process name.
        """
        process_mapping = {
            CitizenshipProcessEnum.RENUNCIATION.value: RenunciationIdentifier,
        }

        identifier_class = process_mapping.get(process_name)
        return self.create_identifier(identifier_class) if identifier_class else None

    def create_identifier(self, identifier_class):
        """
        Create an instance of the identifier class with the required parameters.
        """
        if identifier_class:
            identifier_instance = identifier_class(
                address_code=self.application.work_place, dob=self.application.dob
            )
            return identifier_instance.identifier
        return None

    def log_invalid_process_error(self, process_name):
        """
        Log an error and update the response for an invalid process name.
        """
        error_message = f"Application process: {process_name} does not match any configured application processes."
        self.logger.debug(error_message)
        api_message = APIMessage(
            code=400,
            message="Bad request",
            details=(
                f"Application processes misconfigured. "
                f"{process_name} does not match any configured processes."
            ),
        )
        self.response.status = False
        self.response.messages.append(api_message.to_dict())


class CitizenshipDocumentGeneratorFactory:
    """
    Factory for creating document generators based on the application process.
    """

    @staticmethod
    def create_document_generator(application):
        """
        Create the appropriate document generator based on the application process.
        """
        return CitizenshipDocumentGenerator(application=application)

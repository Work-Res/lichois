import logging

from app.api.common.web import APIMessage, APIResponse
from app.exceptions.identifier_config_not_found import IdentifierConfigNotFound
from app.utils import ApplicationProcesses

from app.identifiers.identifier_scan_register import registrar


class ApplicationDocumentGenerator:

    def __init__(self, application):
        self.application = application
        self.response = APIResponse()
        self.logger = logging.getLogger(__name__)

    def generate_document(self):
        """
        Generate document based on the given process.
        """
        process_name = self.application.proces_name

        # Handle special permits
        if process_name == ApplicationProcesses.SPECIAL_PERMIT.value:
            return self.get_special_permit_identifier()

        # Get the appropriate identifier
        identifier = self.get_identifier(process_name)
        if identifier:
            return identifier
        # Log an error if no valid process found
        self.log_invalid_process_error(process_name)
        return None

    def get_identifier(self, process_name):
        """
        Get the identifier for standard processes based on the process name.
        """
        print("self.application.application_type: ", self.application.application_type)
        identifier_class = registrar.get_registered_class(process_name)
        if not identifier_class:
            raise IdentifierConfigNotFound(
                f"Identifier configuration class not found "
                f"for application type/process name: {self.application.application_type}"
            )
        return self.create_identifier(identifier_class) if identifier_class else None

    def get_special_permit_identifier(self):
        """
        Handle the creation of special permit identifiers.
        """
        handler_class = registrar.get_registered_class(
            self.application.application_type
        )
        if not handler_class:
            raise IdentifierConfigNotFound(
                f"Identifier configuration class not found "
                f"for application type/process name: {self.application.application_type}"
            )
        handler_class = registrar.get_registered_class(
            self.application.application_type
        )
        if not handler_class:
            raise IdentifierConfigNotFound(
                f"Identifier configuration class not found "
                f"for application type/process name: {self.application.application_type}"
            )
        return self.create_identifier(handler_class) if handler_class else None

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


class ApplicationDocumentGeneratorFactory:
    """
    Factory for creating document generators based on the application process.
    """

    @staticmethod
    def create_document_generator(application):
        return ApplicationDocumentGenerator(application=application)

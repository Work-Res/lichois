import os
import logging

from django.db.utils import IntegrityError
from django.db import transaction

from pathlib import Path

from app.api.common.web import APIResponse, APIMessage
from app.utils import ApplicationStatusEnum
from app_personal_details.models import Permit
from workresidentpermit.classes import WorkResidentPermitRenewalHistoryService
from .pre_pupolation_service import PrePopulationService
from .application_service import ApplicationService

from ..exceptions import ApplicationRenewalException

from app.api import RenewalApplicationDTO, NewApplicationDTO

from app.models import (
    ApplicationDocument,
    Application,
    ApplicationRenewal,
    ApplicationVersion,
)
from app_comments.models import Comment
from ..validators import ApplicationRenewalValidator

"""
TODO: NO TESTS, and more tests are required.
"""


class RenewalApplicationService(object):
    """Responsible for creation of an application renewal,  records based on given process name.

    Attributes:
        renewal_application: RenewalApplicationService
    """

    def __init__(self, renewal_application: RenewalApplicationDTO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.response = APIResponse()
        self.renewal_application_dto = renewal_application
        self.previous_application = self.get_previous_application()
        self.new_application_version = None
        self._permit = None
        self.load_permit()
        self.application_document = ApplicationDocument()
        self.validator = ApplicationRenewalValidator(
            permit=self._permit,
<<<<<<< HEAD
            application_type=self.renewal_application_dto.application_type,
=======
            application_type=self.previous_application.application_type,
>>>>>>> 91f1da009e81f0aa5d1dd34c400f34b810daa59b
        )

    def load_permit(self):
        try:
            self.logger.info(
                f"Attempting to load permit with document number: {self.renewal_application_dto.document_number}"
            )
            self._permit = Permit.objects.get(
                document_number=self.renewal_application_dto.document_number
            )
            self.logger.info(
                f"Permit found for document number: {self.renewal_application_dto.document_number}"
            )
        except Permit.DoesNotExist:
            self.logger.warning(
                f"Permit not found for document number: {self.renewal_application_dto.document_number}"
            )
            self._permit = None
        except Exception as e:
            self.logger.error(
                f"Error occurred while loading permit for document number:"
                f" {self.renewal_application_dto.document_number}, Error: {str(e)}",
                exc_info=True,
            )
            raise

        return self._permit

    def get_previous_application(self) -> None:
        """
        Retrieve the previous accepted application based on the renewal application's document number.
        """
        try:
            previous_application = Application.objects.get(
                application_document__document_number=self.renewal_application_dto.document_number,
                application_status__code__iexact=ApplicationStatusEnum.ACCEPTED.value,
            )
        except Application.DoesNotExist:
            error_message = (
                f"An application with status '{ApplicationStatusEnum.ACCEPTED.value}"
                f"does not exist for creating renewal: {self.renewal_application_dto.document_number}."
            )
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details=f"Previous application not found, renewal creation aborted "
                f"- {self.renewal_application_dto.document_number}.",
            )
            self.response.messages.append(api_message.to_dict())
            self.logger.error(error_message)
        except Exception as e:
            self.logger.error(
                f"An unexpected error occurred during renewal creation: {str(e)}"
            )
        else:
            return previous_application

    @transaction.atomic()
    def create_application_renewal(
        self,
        new_application_version: ApplicationVersion = None,
        comment: Comment = None,
        submitted_by=None,
    ):

        if not new_application_version:
            self.logger.error(
                "New application version is required to create a renewal."
            )
            api_message = APIMessage(
                code=400,
                message="Failed to create new renewal application",
                details=f"New application version is required to create a renewal for"
                f" {self.renewal_application_dto.document_number}",
            )
            self.response.messages.append(api_message.to_dict())
            return

        try:
            ApplicationRenewal.objects.create(
                previous_application=self.previous_application,
                renewal_application=new_application_version.application,
                comment=comment,
                submitted_by=submitted_by,
            )
        except IntegrityError as e:
            self.logger.error(
                "An integrity error occurred while creating the application renewal."
            )
            details = f"Failed to create new renewal application for {self.renewal_application_dto.document_number}. Got exception: {str(e)}"
            api_message = APIMessage(
                code=400,
                message="Failed to create new renewal application",
                details=details,
            )
            self.response.messages.append(api_message.to_dict())
            raise ApplicationRenewalException(detail=details)
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {str(e)}")
            details = f"Failed to create new renewal application for {self.renewal_application_dto.document_number}. Got exception: {str(e)}"
            api_message = APIMessage(
                code=400,
                message="Failed to create new renewal application",
                details=details,
            )
            self.response.messages.append(api_message.to_dict())
            raise ApplicationRenewalException(detail=details)

    def create_all(self, new_application_version: ApplicationVersion = None):

        self.logger.info(
            "Starting create_all method with new_application_version: %s",
            new_application_version.application.application_document.document_number,
        )

        if self.validator.is_renewal_allowed():
            try:
                self.logger.info("Creating application renewal.")
                self.renewal_application = self.create_application_renewal(
                    new_application_version=new_application_version
                )
                self.logger.info(
                    "Successfully created renewal application with document_number: %s",
                    self.renewal_application_dto.document_number,
                )

                self.logger.info("Creating renewal application history.")
                WorkResidentPermitRenewalHistoryService(
                    document_number=self.renewal_application_dto.document_number,
                    application_type=self.renewal_application_dto.application_type,
                    application_user=self.previous_application.application_document.applicant,
                    process_name=self.previous_application.process_name,
                ).create_application_renewal_history()
                self.logger.info("Successfully created renewal application history.")

            except Exception as e:
                self.logger.error("Error occurred during create_all method: %s", str(e))
                raise
        else:
            self.logger.warning("Permit has not reached allowable renewable period.")

    def prepare_new_application_dto(self) -> NewApplicationDTO:
        """
        Prepare the DTO for the new application based on the previous application data.
        """
        new_application_dto = NewApplicationDTO(
            process_name=self.renewal_application_dto.proces_name,
            applicant_identifier=self.renewal_application_dto.applicant_identifier,
            status=ApplicationStatusEnum.NEW.value,
        )
        new_application_dto.dob = (
            self.previous_application.application_document.applicant.dob
        )
        new_application_dto.full_name = (
            self.previous_application.application_document.applicant.full_name
        )
        new_application_dto.application_type = (
            self.previous_application.application_type
        )
        new_application_dto.work_place = self.renewal_application_dto.work_place
        return new_application_dto

    @transaction.atomic()
    def process_renewal(self):
        """
        1. Check if the process has a predefinition.
        2. If Yes, then prepopulate based on the prepolulation definition.
        3. Create renewal record
        """
        if not self.response.messages:
            new_application_dto = self.prepare_new_application_dto()
            application_service = ApplicationService(
                new_application=new_application_dto
            )
            self.new_application_version = application_service.create_application()
            self.create_application_renewal(
                new_application_version=self.new_application_version
            )

            # self.run_prepopulation() disable prepopulation

            WorkResidentPermitRenewalHistoryService(
                document_number=self.renewal_application_dto.document_number,
                application_type=new_application_dto.application_type,
                application_user=self.previous_application.application_document.applicant,
                process_name=self.previous_application.process_name,
            ).create_application_renewal_history()

    def run_prepopulation(self):
        """
        Run the prepopulation process for the renewal application.

        This method sets up the configuration and runs the prepopulation service
        to populate the new application version with the necessary data given process.
        """

        file_name = "work_permit.json"
        configuration_location = (
            Path(os.getcwd()) / "app_checklist" / "data" / "prepopulation" / file_name
        )

        if not configuration_location.exists():
            self.logger.error(f"Configuration file not found: {configuration_location}")
            return
        try:
            data = {"document_number": self.renewal_application_dto.document_number}
            service = PrePopulationService(
                new_application_version=self.new_application_version,
                configuration_location=configuration_location,
                filter_data=data,
            )
            service.prepupoluate()
            self.logger.info("Prepopulation completed successfully.")
        except Exception as e:
            self.logger.error(
                f"An error occurred during prepopulation: {str(e)}", exc_info=True
            )

import os
import logging

from django.db.utils import IntegrityError
from django.db import models, transaction

from pathlib import Path

from app.api.common.web import APIResponse, APIMessage
from app.utils import ApplicationStatuses
from .pre_pupolation_service import PrePopulationService
from .create_new_application_service import CreateNewApplicationService

from ..exceptions import ApplicationRenewalException

from app.api import RenewalApplicationDTO, NewApplicationDTO

from app.models import (ApplicationDocument, Application, ApplicationRenewal, ApplicationVersion)
from app_comments.models import Comment

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
        self.response = APIResponse()
        self.renewal_application = renewal_application
        self.previous_application = self.get_previous_application()
        self.new_application_version = None
        self.application_document = ApplicationDocument()

    def get_previous_application(self) -> None:
        """
        Retrieve the previous accepted application based on the renewal application's document number.
        """
        try:
            previous_application = Application.objects.get(
                application_document__document_number=self.renewal_application.document_number,
                application_status__code__iexact=ApplicationStatuses.ACCEPTED.value
            )
        except Application.DoesNotExist:
            error_message = (
                f"An application with status '{ApplicationStatuses.ACCEPTED.value}' does not exist for creating renewal: "
                f"{self.renewal_application.document_number}."
            )
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details=f"Previous application not found, renewal creation aborted - {self.renewal_application.document_number}."
            )
            self.response.messages.append(api_message.to_dict())
            self.logger.error(error_message)
        except Exception as e:
            self.logger.error(f"An unexpected error occurred during renewal creation: {str(e)}")
        else:
            return previous_application

    @transaction.atomic()
    def create_application_renewal(self,
                                   new_application_version: ApplicationVersion = None,
                                   comment: Comment = None,
                                   submitted_by=None):

        if not new_application_version:
            self.logger.error("New application version is required to create a renewal.")
            api_message = APIMessage(
                code=400,
                message="Failed to create new renewal application",
                details=f"New application version is required to create a renewal for {self.renewal_application.document_number}"
            )
            self.response.messages.append(api_message.to_dict())
            return

        try:
            ApplicationRenewal.objects.create(
                previous_application=self.previous_application,
                renewal_application=new_application_version.application,
                comment=comment,
                submitted_by=submitted_by
            )
        except IntegrityError as e:
            self.logger.error("An integrity error occurred while creating the application renewal.")
            details = f"Failed to create new renewal application for {self.renewal_application.document_number}. Got exception: {str(e)}"
            api_message = APIMessage(
                code=400,
                message="Failed to create new renewal application",
                details=details
            )
            self.response.messages.append(api_message.to_dict())
            raise ApplicationRenewalException(detail=details)
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {str(e)}")
            details = f"Failed to create new renewal application for {self.renewal_application.document_number}. Got exception: {str(e)}"
            api_message = APIMessage(
                code=400,
                message="Failed to create new renewal application",
                details=details
            )
            self.response.messages.append(api_message.to_dict())
            raise ApplicationRenewalException(detail=details)

    def prepare_new_application_dto(self) -> NewApplicationDTO:
        """
        Prepare the DTO for the new application based on the previous application data.
        """
        new_application_dto = NewApplicationDTO()
        new_application_dto.status = ApplicationStatuses.NEW.value
        new_application_dto.applicant_identifier = self.renewal_application.applicant_identifier
        new_application_dto.proces_name = self.renewal_application.proces_name
        new_application_dto.dob = self.previous_application.application.application_document.applicant.dob
        new_application_dto.full_name = self.previous_application.application.application_document.applicant.full_name
        new_application_dto.application_type = self.previous_application.application.application_type
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
            application_service = CreateNewApplicationService(new_application=new_application_dto)
            self.new_application_version = application_service.create()
            self.create_application_renewal(new_application_version=self.new_application_version)
            # self.run_prepopulation() disable prepopulation

    def run_prepopulation(self):
        """
        Run the prepopulation process for the renewal application.

        This method sets up the configuration and runs the prepopulation service
        to populate the new application version with the necessary data given process.
        """

        file_name = "work_permit.json"
        configuration_location = Path(os.getcwd()) / "app_checklist" / "data" / "prepopulation" / file_name

        if not configuration_location.exists():
            self.logger.error(f"Configuration file not found: {configuration_location}")
            return
        try:
            data = {
                "document_number": self.renewal_application.document_number
            }
            service = PrePopulationService(
                new_application_version=self.new_application_version, configuration_location=configuration_location,
                filter_data=data
            )
            service.prepupoluate()
            self.logger.info("Prepopulation completed successfully.")
        except Exception as e:
            self.logger.error(f"An error occurred during prepopulation: {str(e)}", exc_info=True)

from random import randint
from django.test import TestCase
from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.models import ApplicationStatus
from app.utils import ApplicationStatusEnum, statuses
from citizenship.utils import CitizenshipProcessEnum


class BaseTest(TestCase):
    """
    Base test class providing common setup and utility methods for application-related tests.
    """

    def setUp(self):
        """
        Common setup tasks for all tests.
        """
        self.create_application_statuses()

    def create_new_application(self, process_name=CitizenshipProcessEnum.RENUNCIATION.value,
                               applicant_identifier=None, status=ApplicationStatusEnum.VERIFICATION.value,
                               dob="06101990", work_place="01", application_type=CitizenshipProcessEnum.RENUNCIATION.value,
                               full_name="Test test"):
        """
        Helper method to create a new application.
        :param process_name: Name of the process.
        :param applicant_identifier: Identifier for the applicant.
        :param status: Status of the application.
        :param dob: Date of birth of the applicant.
        :param work_place: Work place of the applicant.
        :param application_type: Type of the application.
        :param full_name: Full name of the applicant.
        :return: Created application instance.
        """
        if not applicant_identifier:
            applicant_identifier = f'{randint(1, 9)}1791851{randint(1, 9)}'

        self.new_application_dto = NewApplicationDTO(
            process_name=process_name,
            applicant_identifier=applicant_identifier,
            status=status,
            dob=dob,
            work_place=work_place,
            application_type=application_type,
            full_name=full_name
        )
        self.application_service = ApplicationService(
            new_application_dto=self.new_application_dto)
        return self.application_service.create_application()

    def create_application_statuses(self):
        """
        Helper method to create application statuses from predefined statuses.
        """
        for status in statuses:
            ApplicationStatus.objects.create(
                **status
            )


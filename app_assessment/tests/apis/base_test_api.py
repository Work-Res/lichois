from random import randint

from rest_framework.test import APITestCase

from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.models import ApplicationStatus
from app.utils import ApplicationStatusEnum, statuses
from citizenship.utils import CitizenshipProcessEnum


class BaseTestAPI(APITestCase):

    def setUp(self):
        """
        Common setup tasks for all tests.
        """
        self.create_application_statuses()

    def create_new_application(self):
        self.new_application_dto = NewApplicationDTO(
            process_name=CitizenshipProcessEnum.RENUNCIATION.value,
            applicant_identifier=f'{randint(1, 9)}1791851{randint(1, 9)}',
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=CitizenshipProcessEnum.RENUNCIATION.value,
            full_name="Test test",
            applicant_type="student"
        )
        self.application_service = ApplicationService(
            new_application_dto=self.new_application_dto)
        return self.application_service.create_application()

    def create_application_statuses(self):
        for status in statuses:
            ApplicationStatus.objects.create(
                **status
            )

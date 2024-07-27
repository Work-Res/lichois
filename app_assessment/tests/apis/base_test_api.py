from rest_framework.test import APITestCase

from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.utils import ApplicationStatusEnum
from citizenship.utils import CitizenshipProcessEnum


class BaseTestAPI(APITestCase):

    def create_new_application(self):
        self.new_application_dto = NewApplicationDTO(
            process_name=CitizenshipProcessEnum.RENUNCIATION.value,
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.NEW.value,
            dob="06101990",
            work_place="01",
            application_type=CitizenshipProcessEnum.RENUNCIATION.value,
            full_name="Test test"
        )
        self.application_service = ApplicationService(
            new_application_dto=self.new_application_dto)
        return self.application_service.create_application()

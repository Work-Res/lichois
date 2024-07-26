from app.models import Application
from app.utils import ApplicationStatusEnum
from .base_setup import BaseSetup
from app.api import NewApplicationDTO

from app.classes import ApplicationService
from ..utils import CitizenshipProcessEnum


class TestDeclarationOfIntentionByForeignWorkflow(BaseSetup):

    def create_new_application(self):
        self.new_application_dto = NewApplicationDTO(
            process_name=CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value,
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.NEW.value,
            dob="06101990",
            work_place="01",
            application_type=CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value,
            full_name="Test test"
        )

        self.application_service = ApplicationService(
            new_application_dto=self.new_application_dto)
        return self.application_service.create_application()

    def test_create_new_application(self):

        """Test create workflow application. """
        app = Application.objects.get(
            application_document__document_number=self.document_number)
        self.assertEqual(app.process_name, CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value)

    def test_system_verification(self):
        """Test create workflow application. """
        app = Application.objects.get(
            application_document__document_number=self.document_number)
        self.assertEqual(app.process_name, CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value)

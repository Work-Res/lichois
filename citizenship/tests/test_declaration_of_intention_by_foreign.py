from app.api.dto import ApplicationVerificationRequestDTO
from app.models import Application
from app.service import VerificationService
from app.utils import ApplicationStatusEnum
from app_checklist.models import Classifier, ClassifierItem, SystemParameter
from app_decision.models import ApplicationDecision
from app_personal_details.models import Permit
from .base_setup import BaseSetup
from app.api import NewApplicationDTO

from app.classes import ApplicationService
from ..utils import CitizenshipProcessEnum


class TestDeclarationOfIntentionByForeignWorkflow(BaseSetup):

    def setUp(self) -> None:
        super().setUp()

    def create_new_application(self):
        self.new_application_dto = NewApplicationDTO(
            process_name=CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value,
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value,
            full_name="Test test",
            applicant_type="student"
        )

        self.application_service = ApplicationService(
            new_application_dto=self.new_application_dto)
        return self.application_service.create_application()

    def test_check_if_workflow_created_as_expected(self):

        """Test create workflow application. """
        app = Application.objects.get(
            application_document__document_number=self.document_number)
        self.assertEqual(app.process_name, CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value)
        classifier = Classifier.objects.get(code=self.application.process_name)
        self.assertIsNotNone(classifier)
        steps = ClassifierItem.objects.filter(classifier=classifier)
        self.assertEqual(steps.count(), 2)

    def test_submit_officer_verification_and_issued_production(self):
        """Test if application can submit for verification, and then  """

        SystemParameter.objects.create(
            application_type=CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value,
            duration_type="months",
            duration=30
        )

        verification_request = ApplicationVerificationRequestDTO(
            document_number=self.document_number,
            user="test",
            status="ACCEPTED",
        )
        service = VerificationService(verification_request=verification_request)
        data = service.create_verification()

        app = Application.objects.get(
            application_document__document_number=self.document_number)

        self.assertEqual(app.process_name, CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value)
        self.assertEqual(app.application_status.code.upper(), "ACCEPTED")

        application_decision = ApplicationDecision.objects.filter(document_number=self.document_number)
        self.assertTrue(application_decision.exists())

        permit = Permit.objects.filter(document_number=self.document_number)
        self.assertTrue(permit.exists())

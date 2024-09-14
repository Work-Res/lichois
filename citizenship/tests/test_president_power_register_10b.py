from django.test import tag
from app.api.dto import ApplicationVerificationRequestDTO
from app.models import Application
from app.service import VerificationService
from app.utils import ApplicationStatusEnum

from faker import Faker

from app_checklist.models import Classifier, ClassifierItem, SystemParameter

from app_decision.models import ApplicationDecision
from app_personal_details.models import Permit
from workflow.models import Activity
from .base_setup import BaseSetup
from app.api import NewApplicationDTO

from app.classes import ApplicationService
from ..utils import CitizenshipProcessEnum


@tag('pp10b')
class TestPresidentPowerToRegister10bWorkflow(BaseSetup):

    def setUp(self) -> None:
        super().setUp()

    def create_new_application(self):
        self.new_application_dto = NewApplicationDTO(
            process_name=CitizenshipProcessEnum.PRESIDENT_POWER_10B.value,
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=CitizenshipProcessEnum.PRESIDENT_POWER_10B.value,
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
        self.assertEqual(app.process_name, CitizenshipProcessEnum.PRESIDENT_POWER_10B.value)
        classifier = Classifier.objects.get(code=self.application.process_name)
        self.assertIsNotNone(classifier)
        steps = ClassifierItem.objects.filter(classifier=classifier)
        self.assertEqual(steps.count(), 9)

        activites = Activity.objects.filter(
            process__document_number=self.document_number
        ).order_by("sequence")
        self.assertEqual(activites[0].name, "VERIFICATION")
        self.assertEqual(activites[1].name, "VETTING")
        self.assertEqual(activites[2].name, "ASSESSMENT")
        self.assertEqual(activites[3].name, "REVIEW")
        self.assertEqual(activites[4].name, "RECOMMENDATION")
        self.assertEqual(activites[5].name, "PS_RECOMMENDATION")
        self.assertEqual(activites[6].name, "PRES_PS_RECOMMENDATION")
        self.assertEqual(activites[7].name, "PRES_PS_RECOMMENDATION")
        self.assertEqual(activites[8].name, "PRES_PS_RECOMMENDATION")

    def test_submit_officer_verification_and_move_production(self):
        """Test if application can submit for verification, and then  """

        SystemParameter.objects.create(
            application_type=CitizenshipProcessEnum.PRESIDENT_POWER_10A.value,
            duration_type="years",
            duration=2
        )

        faker = Faker()

        verification_request = ApplicationVerificationRequestDTO(
            document_number=self.document_number,
            user="test",
            status="ACCEPTED",
        )
        service = VerificationService(verification_request=verification_request)
        service.create_verification()
        app = Application.objects.get(
            application_document__document_number=self.document_number)
        app.refresh_from_db()
        self.assertEqual(app.process_name, CitizenshipProcessEnum.PRESIDENT_POWER_10A.value)

        self.assertEqual(app.application_status.code.upper(), "ACCEPTED")

        application_decision = ApplicationDecision.objects.filter(document_number=self.document_number)
        self.assertTrue(application_decision.exists())

        permit = Permit.objects.filter(document_number=self.document_number)
        self.assertTrue(permit.exists())
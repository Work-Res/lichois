from app.models import Application, ApplicationDecision

from app.utils import ApplicationStatusEnum
from app_checklist.models import Classifier, ClassifierItem, SystemParameter
from app_personal_details.models import Permit
from workflow.models import Activity
from .base_setup import BaseSetup
from app.api import NewApplicationDTO

from app.classes import ApplicationService
from ..utils import CitizenshipProcessEnum

from ..utils.citizenship_stages_enum import CitizenshipStagesEnum


class TestResumptionCitizenship(BaseSetup):

    def setUp(self) -> None:
        super().setUp()

    def create_new_application(self):
        self.new_application_dto = NewApplicationDTO(
            process_name=CitizenshipProcessEnum.CITIZENSHIP_RESUMPTION.value,
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=CitizenshipProcessEnum.CITIZENSHIP_RESUMPTION.value,
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
        self.assertEqual(app.process_name, CitizenshipProcessEnum.CITIZENSHIP_RESUMPTION.value)
        classifier = Classifier.objects.get(code=self.application.process_name)
        self.assertIsNotNone(classifier)
        steps = ClassifierItem.objects.filter(classifier=classifier)
        self.assertEqual(steps.count(), 4)
        activites = Activity.objects.filter(
            process__document_number=self.document_number
        ).order_by("sequence")
        self.assertEqual(activites[0].name, "VERIFICATION")
        self.assertEqual(activites[1].name, "RECOMMENDATION")
        self.assertEqual(activites[2].name, "MINISTER_DECISION")
        self.assertEqual(activites[3].name, "FINAL_DECISION")

    def test_workflow_transaction_after_when_performing_recommendation(self):

        SystemParameter.objects.create(
            application_type=CitizenshipProcessEnum.CITIZENSHIP_RESUMPTION.value,
            duration_type="years",
            duration=100
        )

        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, CitizenshipProcessEnum.CITIZENSHIP_RESUMPTION.value)
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value
        )

        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.RECOMMENDATION.value.lower()
        )

        self.assertIsNotNone(self.perform_recommendation())
        app.refresh_from_db()
        self.assertEqual(app.recommendation, "ACCEPTED")
        self.assertEqual(app.application_status.code.upper(), "MINISTER_DECISION")

        self.assertIsNotNone(self.perform_minister_decision())
        app.refresh_from_db()

        application_decision = ApplicationDecision.objects.filter(document_number=self.document_number)
        self.assertTrue(application_decision.exists())

        permit = Permit.objects.filter(document_number=self.document_number)
        self.assertTrue(permit.exists())

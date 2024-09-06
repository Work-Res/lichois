from django.test import tag

from app.models import Application
from app.utils import ApplicationStatusEnum
from app_checklist.models import Classifier, ClassifierItem
from app_decision.models import ApplicationDecision
from app_personal_details.models import Permit
from workflow.models import Activity
from .base_setup import BaseSetup
from app.api import NewApplicationDTO

from app.classes import ApplicationService
from ..utils import CitizenshipProcessEnum

from ..utils.citizenship_stages_enum import CitizenshipStagesEnum


@tag('mpw')
class TestMaturityPeriodWaiverWorkflow(BaseSetup):

    def setUp(self) -> None:
        super().setUp()

    def create_new_application(self):
        self.new_application_dto = NewApplicationDTO(
            process_name=CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value,
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value,
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
        self.assertEqual(app.process_name, CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value)
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

    def test_submit_officer_verification_and_move_recommandation(self):
        """Test if application can submit for verification, and then  """

        self.assertIsNotNone(self.perform_verification())

        app = Application.objects.get(
            application_document__document_number=self.document_number)

        self.assertEqual(app.process_name, CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value)
        self.assertEqual(app.application_status.code.upper(), "RECOMMENDATION")

    def test_submit_officer_verification_and_complete_recommedation(self):
        """Test if application can submit for verification, and then  """

        self.assertIsNotNone(self.perform_verification())

        app = Application.objects.get(application_document__document_number=self.document_number)

        self.assertEqual(app.process_name, CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value)
        self.assertEqual(app.application_status.code.upper(), CitizenshipStagesEnum.RECOMMENDATION.value.upper())

        self.assertIsNotNone(self.perform_recommendation())
        app.refresh_from_db()

        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.MINISTER_DECISION.value.lower())

    def test_submit_officer_verification_and_complete_minister_decision(self):
        """Test if application can submit for verification, and then  """

        self.assertIsNotNone(self.perform_verification())

        app = Application.objects.get(application_document__document_number=self.document_number)

        self.assertEqual(app.process_name, CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value)
        self.assertEqual(app.application_status.code.upper(), CitizenshipStagesEnum.RECOMMENDATION.value.upper())

        self.assertIsNotNone(self.perform_recommendation())
        app.refresh_from_db()

        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.MINISTER_DECISION.value.lower())

        self.assertIsNotNone(self.perform_minister_decision())
        app.refresh_from_db()

        self.assertEqual(app.application_status.code.upper(), "ACCEPTED")

        application_decision = ApplicationDecision.objects.filter(document_number=self.document_number)
        self.assertTrue(application_decision.exists())

        permit = Permit.objects.filter(document_number=self.document_number)
        self.assertTrue(permit.exists())

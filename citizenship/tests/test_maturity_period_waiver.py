from django.test import tag

from app.models import Application
from app.utils import ApplicationStatusEnum
from app_checklist.models import Classifier, ClassifierItem, SystemParameter
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
        self.assertEqual(steps.count(), 6)

        activites = Activity.objects.filter(
            process__document_number=self.document_number
        ).order_by("sequence")

        self.assertEqual(activites[0].name, "VERIFICATION")
        self.assertEqual(activites[1].name, "ASSESSMENT")
        self.assertEqual(activites[2].name, "REVIEW")
        self.assertEqual(activites[3].name, "RECOMMENDATION")
        self.assertEqual(activites[4].name, "MINISTER_DECISION")
        self.assertEqual(activites[5].name, "FINAL_DECISION")

    # test_workflow_transaction_when_performing_review

    def test_submit_officer_verification_and_move_recommandation(self):
        """Test if application can submit for verification, and then  """

        self.assertIsNotNone(self.perform_verification())

        app = Application.objects.get(
            application_document__document_number=self.document_number)

        self.assertEqual(app.process_name, CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value)
        self.assertEqual(app.application_status.code.upper(), "ASSESSMENT")

    def test_workflow_transaction_when_performing_review(self):
        # verification
        app = Application.objects.get(
            application_document__document_number=self.document_number)

        self.assertEqual(app.process_name, CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value)
        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value)

        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")
        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.ASSESSMENT.value.lower())

        # assessment
        self.assertIsNotNone(self.perform_assessment())
        app.refresh_from_db()
        self.assertEqual(app.assessment, "ACCEPTED")
        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.REVIEW.value.lower())

        # review
        self.assertIsNotNone(self.perform_review())
        app.refresh_from_db()
        self.assertEqual(app.review, "ACCEPTED")
        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.RECOMMENDATION.value.lower(),)

    def test_submit_officer_verification_and_complete_recommedation(self):
        """Test if application can submit for verification, and then  """

        self.assertIsNotNone(self.perform_verification())

        app = Application.objects.get(application_document__document_number=self.document_number)

        self.assertEqual(app.process_name, CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value)
        self.assertEqual(app.application_status.code.upper(), CitizenshipStagesEnum.ASSESSMENT.value.upper())

        self.assertIsNotNone(self.perform_assessment())
        app.refresh_from_db()
        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.REVIEW.value.lower())

        self.assertIsNotNone(self.perform_review())
        app.refresh_from_db()
        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.RECOMMENDATION.value.lower())

    def test_submit_officer_verification_and_complete_minister_decision_accepted(self):
        """Test if application can submit for verification, and then  """
        SystemParameter.objects.create(
            application_type=CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value,
            duration_type="years",
            duration=100
        )

        self.assertIsNotNone(self.perform_verification())

        app = Application.objects.get(application_document__document_number=self.document_number)

        self.assertEqual(app.process_name, CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value)
        self.assertEqual(app.application_status.code.upper(), CitizenshipStagesEnum.ASSESSMENT.value.upper())

        self.assertIsNotNone(self.perform_assessment())
        app.refresh_from_db()
        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.REVIEW.value.lower())

        self.assertIsNotNone(self.perform_review())
        app.refresh_from_db()
        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.RECOMMENDATION.value.lower(),)


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

    def test_submit_officer_verification_and_complete_minister_decision_rejected(self):
        """Test if application can submit for verification, and then  """
        SystemParameter.objects.create(
            application_type=CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value,
            duration_type="years",
            duration=100
        )

        self.assertIsNotNone(self.perform_verification())

        app = Application.objects.get(application_document__document_number=self.document_number)

        self.assertEqual(app.process_name, CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value)
        self.assertEqual(app.application_status.code.upper(), CitizenshipStagesEnum.ASSESSMENT.value.upper())

        self.assertIsNotNone(self.perform_assessment())
        app.refresh_from_db()
        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.REVIEW.value.lower())

        self.assertIsNotNone(self.perform_review())
        app.refresh_from_db()
        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.RECOMMENDATION.value.lower(),)


        self.assertIsNotNone(self.perform_recommendation())
        app.refresh_from_db()

        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.MINISTER_DECISION.value.lower())

        self.assertIsNotNone(self.perform_minister_decision_reject())
        app.refresh_from_db()

        self.assertEqual(app.application_status.code.upper(), "REJECTED")

        application_decision = ApplicationDecision.objects.filter(document_number=self.document_number)
        self.assertTrue(application_decision.exists())

        permit = Permit.objects.filter(document_number=self.document_number)
        self.assertTrue(permit.exists())

from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.models import Application
from django.test import tag

from app.utils import ApplicationStatusEnum
from app_checklist.models import SystemParameter
from app_decision.models import ApplicationDecision
from app_personal_details.models import Permit
from workflow.models import Activity
from .base_setup import BaseSetup

from ..utils import CitizenshipProcessEnum
from ..utils.citizenship_stages_enum import CitizenshipStagesEnum


@tag("renunc")
class TestSettlementWorkflow(BaseSetup):

    def setUp(self) -> None:
        super().setUp()

    def create_new_application(self):
        self.new_application_dto = NewApplicationDTO(
            process_name=CitizenshipProcessEnum.SETTLEMENT.value,
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=CitizenshipProcessEnum.SETTLEMENT.value,
            full_name="Test test",
            applicant_type="student"
        )

        self.application_service = ApplicationService(
            new_application_dto=self.new_application_dto)
        return self.application_service.create_application()

    @tag("renunc2")
    def test_create_new_application_workflow_records(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, CitizenshipProcessEnum.SETTLEMENT.value)
        activites = Activity.objects.filter(
            process__document_number=self.document_number
        )
        self.assertEqual(6, activites.count())
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value
        )

    @tag("renunc3")
    def test_workflow_transaction_after_when_performing_verification(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, CitizenshipProcessEnum.SETTLEMENT.value)
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value
        )
        activites = Activity.objects.filter(
            process__document_number=self.document_number
        ).order_by("sequence")
        self.assertEqual(activites[0].name, "VERIFICATION")
        self.assertEqual(activites[1].name, "ASSESSMENT")
        self.assertEqual(activites[2].name, "REVIEW")
        self.assertEqual(activites[3].name, "RECOMMENDATION")
        self.assertEqual(activites[4].name, "MINISTER_DECISION")
        self.assertEqual(activites[5].name, "FINAL_DECISION")

        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.ASSESSMENT.value.lower()
        )

    @tag("renunc4")
    def test_workflow_transaction_after_when_performing_assessment(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, CitizenshipProcessEnum.SETTLEMENT.value)
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value
        )

        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.ASSESSMENT.value.lower()
        )

        self.assertIsNotNone(self.perform_assessment())
        app.refresh_from_db()
        self.assertEqual(app.assessment, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.REVIEW.value.lower()
        )

    @tag("renunc5")
    def test_workflow_transaction_after_when_performing_review(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, CitizenshipProcessEnum.SETTLEMENT.value)
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value
        )

        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.ASSESSMENT.value.lower()
        )

        self.assertIsNotNone(self.perform_assessment())
        app.refresh_from_db()
        self.assertEqual(app.assessment, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.REVIEW.value.lower()
        )

        self.assertIsNotNone(self.perform_review())
        app.refresh_from_db()
        self.assertEqual(app.review, "ACCEPTED")
        self.assertEqual(
            app.application_status.code,
            CitizenshipStagesEnum.RECOMMENDATION.value.lower(),
        )


    @tag("renunc6")
    def test_workflow_transaction_after_when_performing_recommandation(self):

        SystemParameter.objects.create(
            application_type=CitizenshipProcessEnum.SETTLEMENT.value,
            duration_type="years",
            duration=100
        )

        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, CitizenshipProcessEnum.SETTLEMENT.value)
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value
        )

        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.ASSESSMENT.value.lower()
        )

        self.assertIsNotNone(self.perform_assessment())
        app.refresh_from_db()
        self.assertEqual(app.assessment, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.REVIEW.value.lower()
        )

        self.assertIsNotNone(self.perform_review())
        app.refresh_from_db()
        self.assertEqual(app.review, "ACCEPTED")
        self.assertEqual(
            app.application_status.code,
            CitizenshipStagesEnum.RECOMMENDATION.value.lower(),
        )

        self.assertIsNotNone(self.perform_recommendation())
        app.refresh_from_db()
        self.assertEqual(app.review, "ACCEPTED")
        self.assertEqual(
            app.application_status.code,
            CitizenshipStagesEnum.MINISTER_DECISION.value.lower(),
        )

        self.assertIsNotNone(self.perform_minister_decision())
        app.refresh_from_db()

        application_decision = ApplicationDecision.objects.filter(document_number=self.document_number)
        self.assertTrue(application_decision.exists())

        permit = Permit.objects.filter(document_number=self.document_number)
        self.assertTrue(permit.exists())

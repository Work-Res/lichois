from app.models import Application
from django.test import tag
from workflow.models import Activity
from .base_setup import BaseSetup

from ..utils import CitizenshipProcessEnum
from ..utils.citizenship_stages_enum import CitizenshipStagesEnum


@tag("renunc")
class TestRenunciationWorkflow(BaseSetup):

    @tag("renunc1")
    def test_create_new_application(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, CitizenshipProcessEnum.RENUNCIATION.value)

    @tag("renunc2")
    def test_create_new_application_workflow_records(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, CitizenshipProcessEnum.RENUNCIATION.value)
        activites = Activity.objects.filter(
            process__document_number=self.document_number
        )
        self.assertEqual(7, activites.count())
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value
        )

    @tag("renunc3")
    def test_workflow_transaction_after_when_performing_verification(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, CitizenshipProcessEnum.RENUNCIATION.value)
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value
        )
        activites = Activity.objects.filter(
            process__document_number=self.document_number
        ).order_by("sequence")
        self.assertEqual(activites[0].name, "VERIFICATION")
        self.assertEqual(activites[1].name, "ASSESSMENT")
        self.assertEqual(activites[2].name, "REVIEW")
        self.assertEqual(activites[3].name, "RECOMMANDATION")
        self.assertEqual(activites[4].name, "MINISTER_DECISION")
        self.assertEqual(activites[5].name, "FOREIGN_RENUNCIATION")
        self.assertEqual(activites[6].name, "FINAL_DECISION")

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
        self.assertEqual(app.process_name, CitizenshipProcessEnum.RENUNCIATION.value)
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
        self.assertEqual(app.process_name, CitizenshipProcessEnum.RENUNCIATION.value)
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
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, CitizenshipProcessEnum.RENUNCIATION.value)
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
            CitizenshipStagesEnum.RECOMMENDATION.value.lower(),
        )

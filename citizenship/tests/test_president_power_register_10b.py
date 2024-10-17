from django.test import tag
from app.models import Application, ApplicationDecision
from app.utils import ApplicationStatusEnum
from app_personal_details.models import Permit
from ..models import Section10bApplicationDecisions

from ..utils.citizenship_stages_enum import CitizenshipStagesEnum


from app_checklist.models import Classifier, ClassifierItem, SystemParameter

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
        self.assertEqual(activites[7].name, "PRESIDENT_DECISION")
        self.assertEqual(activites[8].name, "FINAL_DECISION")

    def test_workflow_after_verification(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )

        self.assertEqual(app.process_name, CitizenshipProcessEnum.PRESIDENT_POWER_10B.value)
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value
        )

        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")
        self.assertEqual(app.application_status.code.upper(), CitizenshipStagesEnum.VETTING.value.upper())

    def test_workflow_after_vetting(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )

        self.assertEqual(app.process_name, CitizenshipProcessEnum.PRESIDENT_POWER_10B.value)
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value
        )

        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")

        self.assertIsNotNone(self.perform_vetting())
        app.refresh_from_db()
        self.assertEqual(app.security_clearance, "ACCEPTED")

        self.assertIsNotNone(self.perform_assessment())
        app.refresh_from_db()
        self.assertEqual(app.assessment, "ACCEPTED")

        self.assertEqual(app.application_status.code.upper(), CitizenshipStagesEnum.REVIEW.value.upper())

    def test_workflow_after_review(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )

        self.assertEqual(app.process_name, CitizenshipProcessEnum.PRESIDENT_POWER_10B.value)
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value
        )

        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")

        self.assertIsNotNone(self.perform_vetting())
        app.refresh_from_db()
        self.assertEqual(app.security_clearance, "ACCEPTED")

        self.assertIsNotNone(self.perform_assessment())
        app.refresh_from_db()
        self.assertEqual(app.assessment, "ACCEPTED")

        self.assertIsNotNone(self.perform_review())
        app.refresh_from_db()
        self.assertEqual(app.review, "ACCEPTED")

        self.assertEqual(app.application_status.code.upper(), CitizenshipStagesEnum.RECOMMENDATION.value.upper())

    def test_workflow_after_recommendation(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )

        self.assertEqual(app.process_name, CitizenshipProcessEnum.PRESIDENT_POWER_10B.value)
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value
        )

        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")

        self.assertIsNotNone(self.perform_vetting())
        app.refresh_from_db()
        self.assertEqual(app.security_clearance, "ACCEPTED")

        self.assertIsNotNone(self.perform_assessment())
        app.refresh_from_db()
        self.assertEqual(app.assessment, "ACCEPTED")

        self.assertIsNotNone(self.perform_review())
        app.refresh_from_db()
        self.assertEqual(app.review, "ACCEPTED")

        self.assertIsNotNone(self.perform_recommendation())
        app.refresh_from_db()
        self.assertEqual(app.recommendation, "ACCEPTED")

        self.assertEqual(app.application_status.code.upper(), CitizenshipStagesEnum.RECOMMENDATION.value.upper())

    def test_workflow_after_pres_recommendation(self):

        SystemParameter.objects.create(
            application_type=CitizenshipProcessEnum.PRESIDENT_POWER_10B.value,
            duration_type="years",
            duration=100
        )

        app = Application.objects.get(
            application_document__document_number=self.document_number
        )

        self.assertEqual(app.process_name, CitizenshipProcessEnum.PRESIDENT_POWER_10B.value)
        self.assertEqual(
            app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value
        )

        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")

        self.assertIsNotNone(self.perform_vetting())
        app.refresh_from_db()
        self.assertEqual(app.security_clearance, "ACCEPTED")

        self.assertIsNotNone(self.perform_assessment())
        app.refresh_from_db()
        self.assertEqual(app.assessment, "ACCEPTED")

        self.assertIsNotNone(self.perform_review())
        app.refresh_from_db()
        self.assertEqual(app.review, "ACCEPTED")

        self.assertEqual(app.application_status.code.upper(), CitizenshipStagesEnum.RECOMMENDATION.value.upper())

        self.assertIsNotNone(self.perform_recommendation())
        app.refresh_from_db()
        self.assertEqual(app.recommendation, "ACCEPTED")

        self.assertEqual(app.application_status.code.upper(), CitizenshipStagesEnum.PS_RECOMMENDATION.value.upper())

        self.assertIsNotNone(self.perform_pres_recommendation(role="PERMANENT_SECRETARY"))

        section10a = Section10bApplicationDecisions.objects.filter(application=app)
        self.assertGreater(section10a.count(), 0)
        app.refresh_from_db()
        section10a_first = section10a.first()
        self.assertEqual(section10a_first.permanent_secretary, "ACCEPTED")

        self.assertEqual(app.application_status.code.upper(),
                         CitizenshipStagesEnum.PRES_PS_RECOMMENDATION.value.upper())

        self.assertIsNotNone(self.perform_pres_recommendation(role="PRES_PERMANENT_SECRETARY"))
        app.refresh_from_db()
        section10a_first.refresh_from_db()

        self.assertEqual(section10a_first.pres_permanent_secretary, "ACCEPTED")

        self.assertEqual(app.application_status.code.upper(),
                         CitizenshipStagesEnum.PRESIDENT_DECISION.value.upper())

        self.assertIsNotNone(self.perform_president_decision())

        application_decision = ApplicationDecision.objects.filter(document_number=self.document_number)
        self.assertTrue(application_decision.exists())

        section10a_first.refresh_from_db()
        self.assertEqual(section10a_first.president_decision, "ACCEPTED")

        permit = Permit.objects.filter(document_number=self.document_number)
        self.assertTrue(permit.exists())

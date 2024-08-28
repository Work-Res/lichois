from django.test import tag
from app.api.dto import ApplicationVerificationRequestDTO
from app.models import Application
from app.service import VerificationService
from app.utils import ApplicationStatusEnum
from app_assessment.models import AssessmentCaseSummary
from app_assessment.service import CaseSummaryService
from app_assessment.service.assessment_case_decision_service import AssessmentCaseDecisionService
from app_checklist.models import Classifier, ClassifierItem
from .base_setup import BaseSetup
from app.api import NewApplicationDTO

from app.classes import ApplicationService
from ..utils import CitizenshipProcessEnum

from app_assessment.api.dto import CaseSummaryRequestDTO, AssessmentCaseDecisionDTO


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
        self.assertEqual(steps.count(), 3)

    def test_submit_officer_verification_and_move_recommandation(self):
        """Test if application can submit for verification, and then  """

        verification_request = ApplicationVerificationRequestDTO(
            document_number=self.document_number,
            user="test",
            status="ACCEPTED",
        )
        service = VerificationService(verification_request=verification_request)
        service.create_verification()

        app = Application.objects.get(
            application_document__document_number=self.document_number)

        self.assertEqual(app.process_name, CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value)
        self.assertEqual(app.application_status.code.upper(), "RECOMMENDATION")

    def test_submit_officer_verification_and_complete_recommedation(self):
        """Test if application can submit for verification, and then  """

        verification_request = ApplicationVerificationRequestDTO(
            document_number=self.document_number,
            user="test",
            status="ACCEPTED",
        )
        service = VerificationService(verification_request=verification_request)
        service.create_verification()

        assessment_comment = CaseSummaryRequestDTO(
            document_number=self.document_number,
            parent_object_id='e8e8e8e8-e8e8-e8e8-e8e8-e8e8e8e8e8e8',
            parent_object_type='app.Application',
            summary="No issues, i recommend"
        )
        assessment_service = CaseSummaryService(case_summary_request_dto=assessment_comment)
        assessment_service.create()
        assessment = AssessmentCaseSummary.objects.get(document_number=self.document_number)
        self.assertIsNotNone(assessment)

        decision_request = AssessmentCaseDecisionDTO(
            document_number=self.document_number,
            parent_object_id=assessment.id,
            parent_object_type='app_assessment.AssessmentCaseSummary',
            author="author",
            author_role="author_role",
            decision="recommended",
        )
        assessment_decison_service = AssessmentCaseDecisionService(assessment_case_decision_dto=decision_request)
        assessment_decison_service.create()

        app = Application.objects.get(application_document__document_number=self.document_number)
        self.assertEqual(app.application_status.code.upper(), "ACCEPTED")

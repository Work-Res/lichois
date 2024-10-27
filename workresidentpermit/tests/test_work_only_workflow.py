from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.models import Application, ApplicationDecision, ApplicationRenewal, ApplicationRenewalHistory, \
    ApplicationReplacement
from app.models.application_replacement_history import ApplicationReplacementHistory

from app.utils import ApplicationStatusEnum, ApplicationProcesses, WorkflowEnum
from app_checklist.models import SystemParameter, SystemParameterPermitRenewalPeriod
from app_personal_details.models import Permit
from workflow.models import Activity
from .base_test_setup import BaseTestSetup


class TestWorkonlyWorkflow(BaseTestSetup):

    def setUp(self) -> None:
        super().setUp()

    def create_new_application(self):
        self.new_application_dto = NewApplicationDTO(
            process_name=ApplicationProcesses.WORK_PERMIT.value,
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=ApplicationProcesses.WORK_PERMIT.value,
            full_name="Test test",
            applicant_type="student"
        )

        self.application_service = ApplicationService(new_application_dto=self.new_application_dto)
        return self.application_service.create_application()

    def test_create_new_application_workflow_records(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, ApplicationProcesses.WORK_PERMIT.value)
        activites = Activity.objects.filter(
            process__document_number=self.document_number
        )
        self.assertEqual(3, activites.count())
        self.assertEqual(
            app.application_status.code, WorkflowEnum.VERIFICATION.value
        )

    def test_workflow_transaction_after_when_performing_board_decision(self):
        SystemParameter.objects.create(
            application_type=ApplicationProcesses.WORK_PERMIT.value,
            duration_type="years",
            duration=100
        )

        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, ApplicationProcesses.WORK_PERMIT.value)
        self.assertEqual(
            app.application_status.code, WorkflowEnum.VERIFICATION.value
        )
        activites = Activity.objects.filter(
            process__document_number=self.document_number
        ).order_by("sequence")
        self.assertEqual(activites[0].name, "VERIFICATION")
        self.assertEqual(activites[1].name, "VETTING")
        self.assertEqual(activites[2].name, "FINAL_DECISION")
        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, WorkflowEnum.VETTING.value.lower()
        )

        self.assertIsNotNone(self.perform_vetting())

        voting_process = self.voting_process()
        self.assertIsNotNone(voting_process)

        application_decision = ApplicationDecision.objects.filter(document_number=self.document_number)
        self.assertTrue(application_decision.exists())
        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ACCEPTED.value.lower()
        )

        permit = Permit.objects.filter(document_number=self.document_number)
        self.assertTrue(permit.exists())

    def test_workflow_transaction_after_when_performing_board_decision_renewal(self):
        SystemParameter.objects.create(
            application_type=ApplicationProcesses.WORK_PERMIT.value,
            duration_type="years",
            duration=100
        )

        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, ApplicationProcesses.WORK_PERMIT.value)
        self.assertEqual(
            app.application_status.code, WorkflowEnum.VERIFICATION.value
        )
        activites = Activity.objects.filter(
            process__document_number=self.document_number
        ).order_by("sequence")
        self.assertEqual(activites[0].name, "VERIFICATION")
        self.assertEqual(activites[1].name, "VETTING")
        self.assertEqual(activites[2].name, "FINAL_DECISION")
        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, WorkflowEnum.VETTING.value.lower()
        )

        self.assertIsNotNone(self.perform_vetting())

        voting_process = self.voting_process()
        self.assertIsNotNone(voting_process)

        application_decision = ApplicationDecision.objects.filter(document_number=self.document_number)
        self.assertTrue(application_decision.exists())
        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ACCEPTED.value.lower()
        )

        permit = Permit.objects.filter(document_number=self.document_number)
        self.assertTrue(permit.exists())

        self.new_application_dto = NewApplicationDTO(
            process_name=ApplicationProcesses.WORK_PERMIT.value,
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=ApplicationProcesses.WORK_PERMIT.value,
            full_name="Test test",
            applicant_type="student",
            application_permit_type="renewal",
            document_number=self.document_number
        )

        SystemParameterPermitRenewalPeriod.objects.create(
            application_type=ApplicationProcesses.WORK_PERMIT.value,
            percent=0.25
        )

        self.application_service = ApplicationService(new_application_dto=self.new_application_dto)
        version = self.application_service.create_application()
        self.assertIsNotNone(version)

        application_renewal = ApplicationRenewal.objects.filter(
            previous_application__application_document__document_number=self.document_number
        )
        self.assertTrue(application_renewal.exists())

        history = ApplicationRenewalHistory.objects.all()
        self.assertTrue(history.exists())

    def test_workflow_transaction_after_when_performing_board_decision_replacement(self):
        SystemParameter.objects.create(
            application_type=ApplicationProcesses.WORK_PERMIT.value,
            duration_type="years",
            duration=100
        )

        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, ApplicationProcesses.WORK_PERMIT.value)
        self.assertEqual(
            app.application_status.code, WorkflowEnum.VERIFICATION.value
        )
        activites = Activity.objects.filter(
            process__document_number=self.document_number
        ).order_by("sequence")
        self.assertEqual(activites[0].name, "VERIFICATION")
        self.assertEqual(activites[1].name, "VETTING")
        self.assertEqual(activites[2].name, "FINAL_DECISION")
        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, WorkflowEnum.VETTING.value.lower()
        )

        self.assertIsNotNone(self.perform_vetting())

        voting_process = self.voting_process()
        self.assertIsNotNone(voting_process)

        application_decision = ApplicationDecision.objects.filter(document_number=self.document_number)
        self.assertTrue(application_decision.exists())
        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ACCEPTED.value.lower()
        )

        permit = Permit.objects.filter(document_number=self.document_number)
        self.assertTrue(permit.exists())

        self.new_application_dto = NewApplicationDTO(
            process_name=ApplicationProcesses.WORK_PERMIT_REPLACEMENT.value,
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=ApplicationProcesses.WORK_PERMIT_REPLACEMENT.value,
            full_name="Test test",
            applicant_type="student",
            application_permit_type="replacement",
            document_number=self.document_number
        )

        self.application_service = ApplicationService(new_application_dto=self.new_application_dto)
        version = self.application_service.create_application()
        self.assertIsNotNone(version)

        application_replacement = ApplicationReplacement.objects.filter(
            previous_application__application_document__document_number=self.document_number
        )
        self.assertTrue(application_replacement.exists())

        history = ApplicationReplacementHistory.objects.all()
        self.assertTrue(history.exists())

        activites = Activity.objects.filter(
            process__document_number=version.application.application_document.document_number
        ).order_by("sequence")

        print(activites)
        self.assertEqual(activites[0].name, "VERIFICATION")
        self.assertEqual(activites[1].name, "FINAL_DECISION")

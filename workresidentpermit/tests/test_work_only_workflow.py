from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.models import Application, ApplicationDecision, ApplicationRenewal, ApplicationRenewalHistory, \
    ApplicationReplacement, ApplicationAppeal
from app.models.application_appeal_history import ApplicationAppealHistory
from app.models.application_replacement_history import ApplicationReplacementHistory

from app.utils import ApplicationStatusEnum, ApplicationProcesses, WorkflowEnum
from app_assessment.models import DependantAssessment, SummaryAssessment
from app_checklist.models import SystemParameter, SystemParameterPermitRenewalPeriod
from app_personal_details.models import Permit
from workflow.models import Activity, Task, WorkflowHistory
from .base_test_setup import BaseTestSetup
from ..api.dto import RequestDeferredApplicationDTO
from ..classes.service import DeferredApplicationService


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
            applicant_type="investor"
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
        self.assertEqual(6, activites.count())
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
        self.assertEqual(activites[1].name, "FEEDBACK")
        self.assertEqual(activites[2].name, "VETTING")
        self.assertEqual(activites[3].name, "ASSESSMENT")
        self.assertEqual(activites[4].name, "FINAL_DECISION")
        self.assertEqual(activites[5].name, "DEFFERED")
        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")

        self.assertEqual(
            app.application_status.code, WorkflowEnum.VETTING.value.lower()
        )

        self.assertIsNotNone(self.perform_vetting())

        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ASSESSMENT.value.lower()
        )

        DependantAssessment.objects.create(
            **{"recommendation": self.document_number, "observation": self.document_number,
               "document_number": self.document_number, "dependent_dob": "1963-05-28",
               "name_of_dependent": "Steven Sarah Williams", "name_of_supporter": "Schultz Joel Lindsay",
               "reason_for_application": "South information red close leg run. Determine rock language put hair."
                                         "Deal approach one research himself modern sell. Question in local.",
               "nationality_of_dependent": "Denmark", "relationship_to_applicant": "Spouse",
               "residential_status_of_supporter": self.document_number,
               "assessment":  "Done"}
        )
        app.refresh_from_db()
        self.assertEqual(app.assessment, "Pending")

        self.assertIsNotNone(self.perform_assessment())

        app.refresh_from_db()
        self.assertEqual(app.assessment, "ACCEPTED")

        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ASSESSMENT.value.lower()
        )

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
        self.assertEqual(activites[1].name, "FEEDBACK")
        self.assertEqual(activites[2].name, "VETTING")
        self.assertEqual(activites[3].name, "ASSESSMENT")
        self.assertEqual(activites[4].name, "FINAL_DECISION")
        self.assertEqual(activites[5].name, "DEFFERED")
        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()

        self.assertEqual(app.verification, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, WorkflowEnum.VETTING.value.lower()
        )

        self.assertIsNotNone(self.perform_vetting())
        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ASSESSMENT.value.lower()
        )

        self.assertIsNotNone(self.perform_assessment())

        app = Application.objects.get(
            application_document__document_number=self.document_number
        )

        self.assertEqual(app.assessment, "ACCEPTED")

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
        app, version = self.application_service.create_application()
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
        self.assertEqual(activites[1].name, "FEEDBACK")
        self.assertEqual(activites[2].name, "VETTING")
        self.assertEqual(activites[3].name, "ASSESSMENT")
        self.assertEqual(activites[4].name, "FINAL_DECISION")
        self.assertEqual(activites[5].name, "DEFFERED")
        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, WorkflowEnum.VETTING.value.lower()
        )

        self.assertIsNotNone(self.perform_vetting())
        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ASSESSMENT.value.lower()
        )

        self.assertIsNotNone(self.perform_assessment())

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
        app, version = self.application_service.create_application()
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
        self.assertEqual(activites[1].name, "FEEDBACK")
        self.assertEqual(activites[2].name, "FINAL_DECISION")

    def test_workflow_transaction_after_when_performing_board_decision_replacement_production(self):
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
        self.assertEqual(activites[1].name, "FEEDBACK")
        self.assertEqual(activites[2].name, "VETTING")
        self.assertEqual(activites[3].name, "ASSESSMENT")
        self.assertEqual(activites[4].name, "FINAL_DECISION")
        self.assertEqual(activites[5].name, "DEFFERED")
        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, WorkflowEnum.VETTING.value.lower()
        )

        self.assertIsNotNone(self.perform_vetting())

        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ASSESSMENT.value.lower()
        )

        self.assertIsNotNone(self.perform_assessment())

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
        app, version = self.application_service.create_application()
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

        self.assertEqual(activites[0].name, "VERIFICATION")
        self.assertEqual(activites[1].name, "FEEDBACK")
        self.assertEqual(activites[2].name, "FINAL_DECISION")

        apps = Application.objects.filter(
            application_document__document_number=version.application.application_document.document_number
        )
        self.assertTrue(apps.exists())

        self.document_number = version.application.application_document.document_number

        SystemParameter.objects.create(
            application_type=ApplicationProcesses.WORK_PERMIT_REPLACEMENT.value,
            duration_type="years",
            duration=100
        )

        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")

        application_decision = ApplicationDecision.objects.filter(document_number=self.document_number)
        self.assertTrue(application_decision.exists())
        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ACCEPTED.value.lower()
        )

        permit = Permit.objects.filter(document_number=self.document_number)
        self.assertTrue(permit.exists())

    def test_workflow_transaction_after_when_performing_board_deferment(self):
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
        self.assertEqual(activites[1].name, "FEEDBACK")
        self.assertEqual(activites[2].name, "VETTING")
        self.assertEqual(activites[3].name, "ASSESSMENT")
        self.assertEqual(activites[4].name, "FINAL_DECISION")
        self.assertEqual(activites[5].name, "DEFFERED")
        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")

        self.assertEqual(
            app.application_status.code, WorkflowEnum.VETTING.value.lower()
        )

        self.assertIsNotNone(self.perform_vetting())

        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ASSESSMENT.value.lower()
        )

        DependantAssessment.objects.create(
            **{"recommendation": self.document_number, "observation": self.document_number,
               "document_number": self.document_number, "dependent_dob": "1963-05-28",
               "name_of_dependent": "Steven Sarah Williams", "name_of_supporter": "Schultz Joel Lindsay",
               "reason_for_application": "South information red close leg run. Determine rock language put hair."
                                         "Deal approach one research himself modern sell. Question in local.",
               "nationality_of_dependent": "Denmark", "relationship_to_applicant": "Spouse",
               "residential_status_of_supporter": self.document_number,
               "assessment":  "Done"}
        )
        app.refresh_from_db()
        self.assertEqual(app.assessment, "Pending")

        self.assertIsNotNone(self.perform_assessment())

        app.refresh_from_db()
        self.assertEqual(app.assessment, "ACCEPTED")

        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ASSESSMENT.value.lower()
        )
        request_deferred_application_dto = RequestDeferredApplicationDTO(
            document_number=self.document_number,
            deferred_from=app.application_status.code,
            expected_action="CORRECTION",
            comment="Correct the assessment"
        )

        service = DeferredApplicationService(
            request_deferred_application_dto=request_deferred_application_dto
        )
        service.create()

        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.DEFERRED.value.lower()
        )

        service.complete_deferred_application()
        
        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ASSESSMENT.value.lower()
        )
        
        # tasks = Task.objects.filter(
        #     activity__process__name__iexact=ApplicationStatusEnum.DEFERRED.value
        # )
        # self.assertTrue(tasks.exists())

        # voting_process = self.voting_process()
        # self.assertIsNotNone(voting_process)
        #
        # application_decision = ApplicationDecision.objects.filter(document_number=self.document_number)
        # self.assertTrue(application_decision.exists())
        # app.refresh_from_db()
        # self.assertEqual(
        #     app.application_status.code, ApplicationStatusEnum.ACCEPTED.value.lower()
        # )
        #
        # permit = Permit.objects.filter(document_number=self.document_number)
        # self.assertTrue(permit.exists())

    def test_workflow_transaction_after_when_performing_board_decision_appeal_production(self):
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
        self.assertEqual(activites[1].name, "FEEDBACK")
        self.assertEqual(activites[2].name, "VETTING")
        self.assertEqual(activites[3].name, "ASSESSMENT")
        self.assertEqual(activites[4].name, "FINAL_DECISION")
        self.assertEqual(activites[5].name, "DEFFERED")
        self.assertIsNotNone(self.perform_verification())
        workflow_history = WorkflowHistory.objects.filter(
            document_number=self.document_number,
            result=True
        )
        self.assertTrue(workflow_history.exists())
        print(workflow_history.first().__dict__)
        self.assertTrue(workflow_history.first().result)

        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")
        self.assertEqual(
            app.application_status.code, WorkflowEnum.VETTING.value.lower()
        )

        self.assertIsNotNone(self.perform_vetting())

        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ASSESSMENT.value.lower()
        )

        self.assertIsNotNone(self.perform_assessment())

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
            process_name=ApplicationProcesses.APPEAL_PERMIT.value,
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=ApplicationProcesses.APPEAL_PERMIT.value,
            full_name="Test test",
            applicant_type="student",
            application_permit_type="appeal",
            document_number=self.document_number
        )

        self.application_service = ApplicationService(new_application_dto=self.new_application_dto)
        app, version = self.application_service.create_application()
        self.assertIsNotNone(version)

        application_appeal = ApplicationAppeal.objects.filter(
            previous_application__application_document__document_number=self.document_number
        )
        self.assertTrue(application_appeal.exists())

        history = ApplicationAppealHistory.objects.all()
        self.assertTrue(history.exists())

        activites = Activity.objects.filter(
            process__document_number=version.application.application_document.document_number
        ).order_by("sequence")

        self.assertEqual(activites[0].name, "VERIFICATION")
        self.assertEqual(activites[1].name, "ASSESSMENT")
        self.assertEqual(activites[2].name, "MINISTER_DECISION")
        self.assertEqual(activites[3].name, "FINAL_DECISION")

        apps = Application.objects.filter(
            application_document__document_number=version.application.application_document.document_number
        )
        self.assertTrue(apps.exists())
        self.document_number = version.application.application_document.document_number

        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, "ACCEPTED")

        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ASSESSMENT.value.lower()
        )

        SummaryAssessment.objects.create(
            **{
                "summary": "Test summary assessment",
                "document_number": self.document_number
            }
        )

        self.assertIsNotNone(self.perform_assessment())

        app.refresh_from_db()
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.MINISTER_DECISION.value.lower()
        )

        SystemParameter.objects.create(
            application_type=ApplicationProcesses.APPEAL_PERMIT.value,
            duration_type="years",
            duration=100
        )

        self.assertIsNotNone(self.perform_minister_decision())

        application_decision = ApplicationDecision.objects.filter(document_number=self.document_number)
        self.assertTrue(application_decision.exists())

        app = Application.objects.get(
            application_document__document_number=version.application.application_document.document_number
        )
        self.assertEqual(
            app.application_status.code, ApplicationStatusEnum.ACCEPTED.value.lower()
        )

        permit = Permit.objects.filter(document_number=self.document_number)
        self.assertTrue(permit.exists())

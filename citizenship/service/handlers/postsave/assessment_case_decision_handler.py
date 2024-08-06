from app.models import Application
from app.workflow import AssessmentCaseDecisionTransactionData
from app_assessment.models import AssessmentCaseDecision

from workflow.classes import TaskDeActivation

from workflow.signals import create_or_update_task_signal


class AssessmentCaseDecisionHandler:

    def __init__(self, assessment_case_decision: AssessmentCaseDecision, role=None):
        self.assessment_case_decision = assessment_case_decision
        self.role = role

    def application(self):
        return Application.objects.get(
            application_document__document_number=self.assessment_case_decision.document_number
        )

    def transaction(self):
        workflow = AssessmentCaseDecisionTransactionData()
        workflow.decision = self.assessment_case_decision.decision
        workflow.role = self.role
        application = self.application()
        stage = application.application_status.code

        create_or_update_task_signal.send(application, source=workflow, application=application)

        task_deactivation = TaskDeActivation(
            application=application,
            source=None,
            model=None
        )
        task_deactivation.update_task_by_activity(name=stage)

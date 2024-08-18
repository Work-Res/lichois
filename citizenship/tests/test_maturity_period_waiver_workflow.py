
from app.models import Application

from workflow.models import Activity
from .base_setup import BaseSetup

from ..utils import CitizenshipProcessEnum
from ..utils.citizenship_stages_enum import CitizenshipStagesEnum


class TestMaturityPeriodWaiverWorkflow(BaseSetup):

    #TODO: 1. submit application
    # 2. officer verification
    # 3. PS recommendation
    # 4. Minister decision
    # 5. Dispatch

    def test_create_new_application(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number)
        self.assertEqual(app.process_name, CitizenshipProcessEnum.RENUNCIATION.value)

    def test_create_new_application_workflow_records(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number)
        self.assertEqual(app.process_name, CitizenshipProcessEnum.RENUNCIATION.value)
        activites = Activity.objects.filter(process__document_number=self.document_number)
        self.assertEqual(7, activites.count())
        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value)

    def test_workflow_transaction_after_when_performing_verification(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number)
        self.assertEqual(app.process_name, CitizenshipProcessEnum.RENUNCIATION.value)
        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value)
        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, CitizenshipStagesEnum.VERIFICATION.value)

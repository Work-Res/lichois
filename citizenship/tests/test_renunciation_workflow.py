
from app.models import Application
from django.test import tag
from workflow.models import Activity
from .base_setup import BaseSetup

from ..utils import CitizenshipProcessEnum
from ..utils.citizenship_stages_enum import CitizenshipStagesEnum

@tag('renunc')
class TestRenunciationWorkflow(BaseSetup):

    @tag('renunc1')
    def test_create_new_application(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number)
        self.assertEqual(app.process_name, CitizenshipProcessEnum.RENUNCIATION.value)

    @tag('renunc2')
    def test_create_new_application_workflow_records(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number)
        self.assertEqual(app.process_name, CitizenshipProcessEnum.RENUNCIATION.value)
        activites = Activity.objects.filter(process__document_number=self.document_number)
        self.assertEqual(7, activites.count())
        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value)

    @tag('renunc3')
    def test_workflow_transaction_after_when_performing_verification(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number)
        self.assertEqual(app.process_name, CitizenshipProcessEnum.RENUNCIATION.value)
        self.assertEqual(app.application_status.code, CitizenshipStagesEnum.VERIFICATION.value)
        self.assertIsNotNone(self.perform_verification())
        app.refresh_from_db()
        self.assertEqual(app.verification, CitizenshipStagesEnum.VERIFICATION.value)

from app.models import Application
from workflow.models import Activity
from .base_setup import BaseSetup

from ..utils import CitizenshipProcessEnum


class TestRenunciationWorkflow(BaseSetup):

    def test_create_new_application(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, CitizenshipProcessEnum.RENUNCIATION.value)

    def test_create_new_application_workflow_records(self):
        app = Application.objects.get(
            application_document__document_number=self.document_number
        )
        self.assertEqual(app.process_name, CitizenshipProcessEnum.RENUNCIATION.value)
        activites = Activity.objects.filter(
            process__document_number=self.document_number
        )
        self.assertEqual(7, activites.count())

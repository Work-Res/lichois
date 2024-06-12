import os

from datetime import date
from unittest.mock import patch

from app.models import Application, ApplicationDocument, ApplicationUser, ApplicationStatus

from workflow.models import BusinessProcess, Activity
from app_checklist.classes import CreateChecklistService

from ..classes import WorkflowEvent

from django.test import TestCase


def application(status):
    try:
        obj = Application.objects.get(application_status__status=status)
        return obj
    except Application.DoesNotExist:
        return None


class TestWorkFlowEvent(TestCase):

    def create_data(self):
        file_name = "work_resident_permit.json"
        output_file = os.path.join(os.getcwd(), "app_checklist", "data", "workflow", file_name)
        service = CreateChecklistService(parent_classifier_name="classifiers", child_name="classifier_items",
                                         foreign_name="classifier",
                                         parent_app_label_model_name="app_checklist.classifier",
                                         foreign_app_label_model_name="app_checklist.classifieritem")

        service.create(file_location=output_file)

        applicant = ApplicationUser(
            full_name="Test test",
            user_identifier="YYYXXX",
            work_location_code="01",
            dob="2000106")
        application_document = ApplicationDocument(
            applicant=applicant,
            document_number="WR0001200202",
            signed_date=date.today(),
            submission_customer="test"
        )
        status = ApplicationStatus(code="NEW")
        app = Application(
            last_application_version_id=1,
            application_document=application_document,
            application_status=status,
            process_name="WORK_RESIDENT_PERMIT"
        )
        return app

    @patch('app.models.Application.objects.get')
    def test_create_workflow(self, application_mock):

        application_mock.return_value = self.create_data()
        event = WorkflowEvent(application=application("NEW"))
        event.create_workflow_process()
        all = BusinessProcess.objects.all()
        self.assertGreater(len(all), 0)

        activities = Activity.objects.filter(process=event.bussiness_process)
        self.assertEqual(len(activities), 3)

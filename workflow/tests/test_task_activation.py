import os
from django.test import TestCase
from unittest.mock import patch
from datetime import date

from ..signals import create_or_update_task_signal
from ..classes import WorkflowEvent

from app.models import Application, ApplicationDocument, ApplicationUser, ApplicationStatus
from app_checklist.classes import CreateChecklist

from workflow.models import Task


def application(status):
    try:
        obj = Application.objects.get(application_status__status=status)
        return obj
    except Application.DoesNotExist:
        return None


class SourceModel:

    def __init__(self, previous_status, current_status=None, next_activity_name=None):
        self.previous_status = previous_status or "NEW"
        self.current_status = current_status
        self.next_activity_name = next_activity_name


class TestTaskActivation(TestCase):

    def create_data(self):
        file_name = "attachment_documents.json"
        output_file = os.path.join(os.getcwd(), "app_checklist", "data", file_name)
        create = CreateChecklist()
        create.create(file_location=output_file)

        applicant = ApplicationUser(
            full_name="Test test",
            user_identifier="YYYXXX",
            work_location_code="01",
            dob="2000106")
        application_document = ApplicationDocument(
            id="abc",
            applicant=applicant,
            document_number="WR0001200202",
            signed_date=date.today(),
            submission_customer="test"
        )
        status = ApplicationStatus(id="abcd", code="NEW")
        app = Application(
            id="yze",
            last_application_version_id=1,
            application_document=application_document,
            application_status=status,
            process_name="WORK_RESIDENT_PERMIT"
        )
        return app

    @patch('app.models.Application.objects.get')
    def test_create_task(self, application_mock):
        application_mock.return_value = self.create_data()
        app = application("NEW")
        event = WorkflowEvent(application=application("NEW"))
        event.create_workflow_process()
        source = SourceModel(
            previous_status="NEW", current_status="VERIFICATION", next_activity_name="SECOND_VERIFICATION")

        create_or_update_task_signal.send(app, source=source, application=app)
        tasks = Task.objects.all()
        self.assertGreater(len(tasks), 0)


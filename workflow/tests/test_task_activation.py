import os
from django.test import TestCase
from unittest.mock import patch
from datetime import date

from ..signals import create_or_update_task_signal
from ..classes import WorkflowEvent
from .data import statuses

from app.models import Application, ApplicationDocument, ApplicationUser, ApplicationStatus

from app_checklist.classes import CreateChecklistService


from workflow.models import Task


def application_status():
    status = ApplicationStatus(id="new", code="NEW")
    return status


def application(status):
    try:
        obj = Application.objects.get(application_status__status=status)
        return obj
    except Application.DoesNotExist:
        return None


class SourceModel:

    def __init__(self, previous_status=None, current_status=None, next_activity_name=None, system_verification=None,
                 application_status=None):
        self.previous_status = previous_status or "NEW"
        self.current_status = current_status
        self.application_status = application_status
        self.next_activity_name = next_activity_name
        self.system_verification = system_verification


class TestTaskActivation(TestCase):

    def create_data(self):

        for status in statuses:
            ApplicationStatus.objects.create(
                **status
            )

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
            id="abc",
            applicant=applicant,
            document_number="WR0001200202",
            signed_date=date.today(),
            submission_customer="test"
        )
        status = ApplicationStatus(id="abcd", code="NEW")
        app = Application(
            last_application_version_id=1,
            application_document=application_document,
            application_status=status,
            process_name="WORK_RESIDENT_PERMIT"
        )
        return app

    @patch('app.models.Application.save')
    @patch('app.models.Application.objects.get')
    def test_create_task_when_all_conditions_valid(self, application_mock, application_save):
        application_mock.return_value = self.create_data()
        app = application("NEW")
        event = WorkflowEvent(application=application("NEW"))
        event.create_workflow_process()

        source = SourceModel(
            application_status="NEW", system_verification="validated", next_activity_name="VETTING")

        create_or_update_task_signal.send(app, source=source, application=app)
        tasks = Task.objects.all()
        self.assertEqual(tasks.count(), 1)
        self.assertGreater(len(tasks), 0)

    @patch('app.models.Application.objects.get')
    @patch('app.models.Application.save')
    def test_create_task_when_not_all_conditions(self, application_mock, application_save):
        application_mock.return_value = self.create_data()
        app = application("NEW")
        event = WorkflowEvent(application=application("NEW"))
        event.create_workflow_process()
        source = SourceModel(
            previous_status="VERIFICATION", current_status="VERIFICATION", next_activity_name="SECOND_VERIFICATION")

        create_or_update_task_signal.send(app, source=source, application=app)
        application_save.assert_called_once()
        tasks = Task.objects.all()
        self.assertEqual(len(tasks), 0)

    @patch('app.models.Application.objects.get')
    def test_create_task_create_second_task(self, application_mock):
        application_mock.return_value = self.create_data()
        app = application("NEW")
        event = WorkflowEvent(application=application("NEW"))
        event.create_workflow_process()
        source = SourceModel(
            previous_status="VERIFICATION", current_status="VERIFICATION", next_activity_name="SECOND_VERIFICATION")

        create_or_update_task_signal.send_robust(app, source=source, application=app)
        tasks = Task.objects.all()
        self.assertEqual(len(tasks), 0)

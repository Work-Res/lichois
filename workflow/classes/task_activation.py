import logging

from typing import TypeVar

from app.utils import ApplicationStatusEnum
from ..rules import workflow
from ..models import Activity, Task
from ..choices import TaskStatus, TaskPriority
from .workflow_application import WorkflowApplication

S = TypeVar("S")
A = TypeVar("A")
M = TypeVar("M")


class TaskActivation:
    """Responsible for creating a new task(s) for a particular application."""

    def __init__(self, source: S, application: A, model: M):
        self.source = source
        self.application = application
        self.model = model
        self.logger = logging.getLogger("workflow")
        self.logger.setLevel(logging.DEBUG)

    def create_task(self):
        """
        Trigger all rules for given process using the application context.
        """
        activities = Activity.objects.filter(
            process__name=self.application.process_name,
            process__document_number=self.application.application_document.document_number,
        )
        for activity in activities:
            self.source.next_activity_name = activity.next_activity_name
            self.logger.info(
                f"{activity.sequence}. Processing next_activity_name {activity.next_activity_name} for "
            )
            self.source.current_status = (
                self.application.application_status.code.upper()
            )
            self.logger.info(
                f"{activity.sequence}. Processing current_status {self.source.current_status} for "
            )
            self.logger.info(f"{activity.sequence}. Source model: {self.source.__dict__}")
            self.logger.info(
                f"{activity.sequence}. activity.create_task_rules: {activity.create_task_rules}"
            )
            if workflow.test_rule(
                activity.name.upper(), self.source, activity.create_task_rules
            ):
                application_status_code = activity.name.upper()
                if activity.name.upper() == "FINAL_DECISION":
                    application_status_code = self.source.status
                WorkflowApplication(
                    application=self.application,
                    application_status_code=application_status_code,
                )
                self.logger.info(
                    f"{activity.sequence}. Attempting to create a new task for "
                    f"{activity.name} - {self.application.application_document.document_number}."
                )
                self.task(activity)
            else:
                self.logger.debug(f"Failed to create task for {activity.name}")

    def task(self, activity):
        try:
            Task.objects.get(activity=activity)
            self.logger.info(
                f"{activity.sequence}. Task already created for {self.application.application_document.document_number}."
            )
        except Task.DoesNotExist:
            Task.objects.create(
                priority=TaskPriority.LOW.value,
                activity=activity,
                status=TaskStatus.NEW.value,
                details=activity.description,
            )
            self.logger.info(
                f"{activity.sequence}. New task has been created for "
                f"{activity.name} - {self.application.application_document.document_number}."
            )

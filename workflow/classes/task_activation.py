import logging

from typing import TypeVar

from ..rules import workflow
from ..models import Activity, Task
from django.db import transaction
from ..choices import TaskStatus, TaskPriority
from .workflow_application import WorkflowApplication
from ..service import WorkflowHistoryService

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
        # self.logger.setLevel(logging.DEBUG)

    @transaction.atomic
    def create_task(self):
        """
        Trigger all rules for given process using the application context.
        """
        activities = Activity.objects.filter(
            process__name=self.application.process_name,
            process__document_number=self.application.application_document.document_number,
            completed=False
        )
        for activity in activities:
            self.source.next_activity_name = activity.next_activity_name
            self.logger.info(
                f"{activity.sequence}. Processing activity {activity.name}"
            )
            self.source.current_status = (
                self.application.application_status.code.upper()
            )
            self.logger.info(
                f"{activity.sequence}. Processing current_status {self.source.current_status} for "
            )
            self.logger.info(
                f"{activity.sequence}. Source model: {self.source.__dict__}"
            )
            self.logger.info(
                f"{activity.sequence}. activity.create_task_rules: {activity.create_task_rules}"
            )
            result = workflow.test_rule(
                activity.name.upper(), self.source, activity.create_task_rules
            )
            if result:
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
                activity.completed = True
                activity.save()
            else:
                self.logger.debug(f"Failed to create task for {activity.name}")
            WorkflowHistoryService.create(
                application=self.application,
                source=self.source,
                create_rule=activity.create_task_rules,
                result=result,
                next_activity_name=activity.next_activity_name
            )

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

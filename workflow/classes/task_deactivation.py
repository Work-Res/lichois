import logging

from typing import TypeVar
from ..models import Activity, Task
from ..choices import TaskStatus

from ..rules import workflow_close


S = TypeVar('S')
A = TypeVar('A')
M = TypeVar('M')


class TaskDeActivation:

    """Responsible for setting a task to closed based on given condition.
    """

    def __init__(self, source: S, application: A, model: M):
        self.source = source
        self.application = application
        self.model = model
        self.logger = logging.getLogger('workflow')

    def update_task(self):
        """
        Trigger all rules for given process using the application context.
        """
        activities = Activity.objects.filter(
            process__name=self.application.process_name,
            process__document_number=self.application.application_document.document_number)
        for activity in activities:
            try:
                task = Task.objects.get(activity=activity)
                if workflow_close.test_rule(activity.name.upper(), self.source, activity.create_rules):
                    task.status = TaskStatus.CLOSED.value
                    task.save()
                    self.logger.info(f"The task {task.id} has been closed. ")
                else:
                    print("Failed to close task for ", activity.name)
            except Task.DoesNotExist:
                pass
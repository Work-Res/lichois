
from django.dispatch import Signal
from django.conf import settings

from workflow.classes import TaskActivation, TaskDeActivation

create_or_update_task_signal = Signal()
update_task_signal = Signal()


def create_task_handler(sender, source=None, application=None,  **kwargs):
    if settings.DEBUG:
        print("Trigger the handler to create the task")
    activation = TaskActivation(source, application, sender)
    activation.create_task()


def close_task_handler(sender, source=None, application=None,  **kwargs):
    deactivation = TaskDeActivation(source, application, sender)
    deactivation.update_task()

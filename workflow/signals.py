
from django.dispatch import Signal

from workflow.classes import TaskActivation, TaskDeActivation

create_or_update_task_signal = Signal()
update_task_signal = Signal()


def create_task_handler(sender, source=None, application=None,  **kwargs):
    activation = TaskActivation(source, application, sender)
    activation.create_task()


def close_task_handler(sender, source=None, application=None,  **kwargs):
    deactivation = TaskDeActivation(source, application, sender)
    deactivation.update_task()

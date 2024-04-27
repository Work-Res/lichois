
from django.dispatch import Signal

from workflow.classes import TaskActivation

create_or_update_task_signal = Signal()


def create_task_handler(sender, source=None, application=None,  **kwargs):
    activation = TaskActivation(source, application, sender)
    activation.create_task()

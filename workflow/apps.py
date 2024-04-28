from django.apps import AppConfig


class WorkflowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workflow'

    def ready(self):
        from .signals import create_or_update_task_signal, create_task_handler, update_task_signal, close_task_handler
        create_or_update_task_signal.connect(create_task_handler)
        update_task_signal.connect(close_task_handler)

import logging

from app.models import Application, ApplicationStatus


class WorkflowApplication:
    """Updates main application stage or status when condition for transistioning is True"""

    def __init__(self, application: Application, application_status_code: str):
        self.logger = logging.getLogger("workflow")
        self.application = application
        self.application_status_code = application_status_code
        self.transition_application()

    def transition_application(self):
        self.logger.info(
            "Workflow:Application, updating it to the next relevant stage."
        )
        print(
            "Workflow:Application, updating it to the next relevant stage.",
            self.application_status_code,
        )
        application_status = ApplicationStatus.objects.get(
            code__iexact=self.application_status_code
        )
        self.application.application_status = application_status
        self.application.save()
        self.logger.info(
            f"Workflow:Application, updating it to the next relevant stage. {self.application.application_status}"
        )

import logging

from workflow.signals import create_or_update_task_signal


class WorkflowManager:
    def __init__(self, workflow, application, logger=None):
        self.workflow = workflow
        self.application = application
        self.logger = logger or logging.getLogger(__name__)

    def activate_next_task(self):
        try:
            if self.workflow:
                self.logger.info(f"Workflow: {self.workflow}, Application: {self.application}")
                create_or_update_task_signal.send_robust(
                    sender=self.application,
                    source=self.workflow,
                    application=self.application,
                )
                self.logger.info("Task signal sent successfully.")
            else:
                self.logger.warning(f"Cannot activate next task. Workflow is missing.")

        except Exception as e:
            self.logger.error(f"Error occurred while activating next task: {str(e)}", exc_info=True)


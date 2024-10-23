import logging
from venv import logger
from django.apps import AppConfig


class AppChecklistConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_checklist"
    verbose_name = "Application Checklist Module"
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def ready(self):
        super().ready()
        try:
            self.setup_logging()
            self.run_initial_configuration()
        except Exception as e:
            logging.error(f"Error during app initialization: {e}")
            raise e

    def setup_logging(self):
        # Configure logging
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
        )
        self.logger.info("Logging is configured.")

    def run_initial_configuration(self):
        from app_checklist.classes import ChecklistSearcherAndUpdater

        self.logger.info("Running initial workflow configuration...")
        try:
            workflow_configs = ChecklistSearcherAndUpdater(
                target_directory_name="workflow"
            )
            workflow_configs.update_workflow()
            logging.info("Workflow configuration updated successfully.")
        except Exception as e:
            logging.error(f"Error during workflow configuration: {e}")

        self.logger.info("Running initial checklist configuration...")
        try:
            searcher = ChecklistSearcherAndUpdater(target_directory_name="checklist")
            searcher.update_checklist()
            logger.info("Checklist configuration updated successfully.")
        except Exception as e:
            logger.error(f"Error during checklist configuration: {e}")

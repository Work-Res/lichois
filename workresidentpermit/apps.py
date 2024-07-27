import logging
from django.apps import AppConfig as BaseAppConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AppConfig(BaseAppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "workresidentpermit"
    verbose_name = "Work Resident Permit Module"

    def ready(self):
        logger.info("Importing signals...")
        from .signals import create_application_final_decision_by_security_clearance

        logger.info("Imported create_application_final_decision_by_security_clearance")
        from .signals import create_application_final_decision_by_commissioner_decision

        logger.info(
            "Imported create_application_final_decision_by_commissioner_decision"
        )
        from .signals import create_application_final_decision_by_minister_decision

        logger.info("Imported create_application_final_decision_by_minister_decision")
        from board.signals import create_application_decision

        logger.info("Imported create_application_decision")
        from .signals import create_production_permit_record

        logger.info("Imported create_production_permit_record")

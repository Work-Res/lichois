import logging

from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "Application Framework Module"
    name = "app"

    def ready(self):
        from app.classes.permissions import GroupCreator
        logger = logging.getLogger(__name__)

        # Import signals (log success or failure)
        try:
            import app.signals
            logger.info("Signals successfully imported.")
        except ImportError as e:
            logger.error("Failed to import signals: %s", e)

        # Scan and register identifier config classes (log success or failure)
        try:
            from app.identifiers.identifier_scan_register import registrar
            registrar.scan_and_register_identifier_config_classes()
            logger.info("Identifier config classes successfully scanned and registered.")
        except ImportError as e:
            logger.error("Failed to import registrar: %s", e)
        except Exception as e:
            logger.error("An error occurred during identifier registration: %s", e)

        # Create or update groups from groups.txt files (log actions)
        try:
            group_creator = GroupCreator()
            group_creator.create_groups_from_files()
            logger.info("Group creation from groups.txt files completed.")
        except Exception as e:
            logger.error("An error occurred during group creation: %s", e)

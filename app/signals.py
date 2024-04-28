import logging

from django.dispatch import receiver
from django.db.models.signals import post_save

from app.models import Application
from workflow.classes import WorkflowEvent


@receiver(post_save, sender=Application)
def create_workflow(sender, instance, created, **kwargs):
    logger = logging.getLogger(__name__)
    try:
        if created:
            WorkflowEvent(application=sender).create_workflow_process()
            logger.info("Created workflow for application: ", sender.application_document.document_number)
            return instance
    except SystemError as e:
        logger.debug("An error occurred while creating workflow, Got ", e)
    except Exception as ex:
        logger.debug("An error occurred while creating workflow, Got ", ex)

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Application, ApplicationVerification
from workflow.classes import WorkflowEvent

from .service import VerificationProductionDecisionService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Application)
def create_workflow(sender, instance, created, **kwargs):
    logger = logging.getLogger(__name__)
    try:
        if created:
            WorkflowEvent(application=instance).create_workflow_process()
            logger.info(
                "Created workflow for application: ",
                instance.application_document.document_number,
            )
            return instance
    except SystemError as e:
        logger.debug("An error occurred while creating workflow, Got ", e)
    except Exception as ex:
        logger.debug("An error occurred while creating workflow, Got ", ex)


@receiver(post_save, sender=ApplicationVerification)
def production_decision_post_save_on_verfication_handler(
    sender, instance, created, **kwargs
):
    if created:
        production_service = VerificationProductionDecisionService(
            document_number=instance.document_number,
            decision_value="ACCEPTED",
        )
        production_service.create_application_decision()
        logger.info(f"Decision created for verification {instance.document_number}")

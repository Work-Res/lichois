import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from app_production.api.dto.permit_request_dto import PermitRequestDTO
from app_production.services.appeal_production_service import AppealProductionService


from .models import Application, ApplicationVerification, MinisterDecision
from workflow.classes import WorkflowEvent

from .service import VerificationProductionDecisionService

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@receiver(post_save, sender=Application)
def create_workflow(sender, instance, created, **kwargs):
    logger = logging.getLogger(__name__)
    try:
        if created:
            WorkflowEvent(application=instance).create_workflow_process()
            # logger.info(
            #     "Created workflow for application: ",
            #     instance.application_document.document_number,
            # )
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


@receiver(post_save, sender=MinisterDecision)
def handle_minister_appeals(sender, instance, created, **kwargs):
    if created and instance.status.code.upper() == "ACCEPTED":
        request = PermitRequestDTO()
        request.document_number = instance.document_number
        request.place_issue = "Gaborone"
        request.security_number = "123456"
        appeal_production_service = AppealProductionService(request=request)
        appeal_production_service.create_new_permit()

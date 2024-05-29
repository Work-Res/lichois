import logging

from django.dispatch import receiver
from django.db.models.signals import post_save

from board.models import BoardDecision

from workresidentpermit.classes import WorkResidentPermitApplicationDecisionService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=BoardDecision)
def create_application_decision(sender, instance, created, **kwargs):
    try:
        if created:
            service = WorkResidentPermitApplicationDecisionService(
                document_number=instance.assessed_application.application_document.document_number,
                board_decision=instance
            )
            service.create()
    except SystemError as e:
        logger.error("SystemError: An error occurred while creating new application decision, Got ", e)
    except Exception as ex:
        logger.error(f"An error occurred while trying to create application decision after saving board decision. "
                     f"Got {ex} ")

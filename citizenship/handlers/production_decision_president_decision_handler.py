import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from app.models import Application
from citizenship.models import CitizenshipMinisterDecision, CitizenshipPresidentDecision
from citizenship.service.production import PresidentProductionDecisionService
from citizenship.service.production.minister_production_decision_service import MinisterProductionDecisionService
from citizenship.service.word import RenunciationDocumentGenerationService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=CitizenshipPresidentDecision)
def production_decision_president_decision_handler(sender, instance, created, **kwargs):
    if not created:
        return

    logger.info(f"President Decision created with ID {instance.id}. Starting processing...")

    try:
        # Create the application decision based on the minister's decision
        production_service = PresidentProductionDecisionService(
            document_number=instance.document_number,
            decision_value=instance.status.code.upper(),
        )
        production_service.create_application_decision()

        logger.info(f"Application decision created for document number {instance.document_number}")


    except ObjectDoesNotExist as e:
        logger.error(f"Application not found for document number {instance.document_number}: {str(e)}")
    except Exception as e:
        logger.exception(f"Unexpected error occurred while handling minister decision for ID {instance.id}: {str(e)}")


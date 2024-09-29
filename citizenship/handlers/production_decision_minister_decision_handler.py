import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from app.models import Application
from citizenship.models import CitizenshipMinisterDecision
from citizenship.service.production.minister_production_decision_service import MinisterProductionDecisionService
from citizenship.service.word import RenunciationDocumentGenerationService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=CitizenshipMinisterDecision)
def production_decision_minister_decision_handler(sender, instance, created, **kwargs):
    # Exit early if not a new record
    if not created:
        return

    logger.info(f"Minister Decision created with ID {instance.id}. Starting processing...")

    try:
        # Create the application decision based on the minister's decision
        production_service = MinisterProductionDecisionService(
            document_number=instance.document_number,
            decision_value=instance.status.code.upper(),
        )
        production_service.create_application_decision()

        logger.info(f"Application decision created for document number {instance.document_number}")

        # Fetch the related application
        application = _get_application(instance.document_number)

        # Create the renunciation letter
        _generate_renunciation_letter(application)


    except ObjectDoesNotExist as e:
        logger.error(f"Application not found for document number {instance.document_number}: {str(e)}")
    except Exception as e:
        logger.exception(f"Unexpected error occurred while handling minister decision for ID {instance.id}: {str(e)}")


def _get_application(document_number):
    """
    Helper function to retrieve the application based on the document number.
    """
    return Application.objects.get(application_document__document_number=document_number)


def _generate_renunciation_letter(application):
    """
    Helper function to handle renunciation document generation.
    """
    service = RenunciationDocumentGenerationService()
    service.handle(application)

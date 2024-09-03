import logging

from app.models import ApplicationVerification, Application
from django.db.models.signals import post_save
from django.dispatch import receiver

from citizenship.service.production import VerificationProductionDecisionService

logger = logging.getLogger(__name__)


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

        logger.info(
            f"ApplicationDecision created for verification on completion ID {instance.id}"
        )

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from citizenship.models import CitizenshipMinisterDecision
from citizenship.service.production.minister_production_decision_service import MinisterProductionDecisionService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=CitizenshipMinisterDecision)
def production_decision_minister_decision_handler(
    sender, instance, created, **kwargs
):
    if created:
        production_service = MinisterProductionDecisionService(
            document_number=instance.document_number,
            decision_value="ACCEPTED",
        )
        production_service.create_application_decision()

        logger.info(
            f"ApplicationDecision created for verification on completion ID {instance.id}"
        )

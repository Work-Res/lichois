import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from citizenship.models import RecommendationDecision
from citizenship.service.production import RecommendationProductionDecisionService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=RecommendationDecision)
def create_production_decision_when_recommendation_completed_handler(sender, instance, created, **kwargs):
    if created:
        production_service = RecommendationProductionDecisionService(
            document_number=instance.document_number,
            decision_value="ACCEPTED",
        )
        # production_service.create_application_decision()

        logger.info(
            f"ApplicationDecision created for verification on completion ID {instance.id}"
        )

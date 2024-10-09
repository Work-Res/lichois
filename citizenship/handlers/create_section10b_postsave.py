import logging
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Application, PresRecommendationDecision
from citizenship.models import Section10bApplicationDecisions

logger = logging.getLogger(__name__)


@receiver(post_save, sender=PresRecommendationDecision)
def pres_recommendation_decision_post_save_handler(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Handling post-save for new PresRecommendationDecision instance: {instance}")

        try:
            with transaction.atomic():
                # Attempt to retrieve the associated application
                application = Application.objects.get(
                    application_document__document_number=instance.document_number
                )
                # Log success if application is found
                logger.info(f"Application found for document_number: {instance.document_number}")

                # Create the Section10bApplicationDecisions object
                decision, created = Section10bApplicationDecisions.objects.get_or_create(
                    application=application
                )
                if created:
                    logger.info(f"New Section10bApplicationDecisions created for application: {application.id}")
                else:
                    logger.info(f"Section10bApplicationDecisions already exists for application: {application.id}")

        except Application.DoesNotExist:
            logger.warning(f"PresRecommendationDecison:No Application found for document_number: {instance.document_number}")

        except Application.MultipleObjectsReturned:
            logger.error(f"Multiple Applications found for document_number: {instance.document_number}")

        except Exception as e:
            logger.error(f"Unexpected error in post-save handler: {e}", exc_info=True)
            # Optionally, re-raise the exception if it's critical
            raise

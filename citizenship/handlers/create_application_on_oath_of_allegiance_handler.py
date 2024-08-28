import logging
from app.utils import ApplicationDecisionEnum
from app_decision.models import ApplicationDecision, ApplicationDecisionType
from citizenship.models import OathOfAllegiance
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


@receiver(post_save, sender=OathOfAllegiance)
def production_decision_post_save_handler(sender, instance, created, **kwargs):
    if created:
        try:
            accepted = ApplicationDecisionType.objects.get(
                code=ApplicationDecisionEnum.ACCEPTED.value
            )
            ApplicationDecision.objects.create(
                document_number=instance.document_number,
                final_decision_type=accepted,
                proposed_decision_type=accepted,
                # comment="president 10a production"
            )
            logger.info(f"ApplicationDecision created for OathOfAllegiance ID {instance.id}")
        except ObjectDoesNotExist:
            logger.error(f"ApplicationDecisionType with code {ApplicationDecisionEnum.ACCEPTED.value} not found.")
        except Exception as e:
            logger.exception(f"Error occurred while creating ApplicationDecision for OathOfAllegiance ID "
                             f"{instance.id}: {str(e)}")

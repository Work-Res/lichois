import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import ApplicationDecision, ApplicationDecisionType
from app.utils import ApplicationDecisionEnum
from citizenship.models import OathOfAllegiance

logger = logging.getLogger(__name__)


@receiver(post_save, sender=OathOfAllegiance)
def production_decision_oathOfAllegiance_post_save_handler(
    sender, instance, created, **kwargs
):
    if created:
        try:
            print("instance instance instance instance", instance.document_number)
            accepted = ApplicationDecisionType.objects.get(
                code=ApplicationDecisionEnum.ACCEPTED.value
            )
            ApplicationDecision.objects.create(
                document_number=instance.document_number,
                final_decision_type=accepted,
                proposed_decision_type=accepted,
                # comment="president 10a production"
            )
            logger.info(
                f"ApplicationDecision created for OathOfAllegiance ID {instance.id}"
            )
        except ObjectDoesNotExist:
            logger.error(
                f"ApplicationDecisionType with code {ApplicationDecisionEnum.ACCEPTED.value} not found."
            )
        except Exception as e:
            logger.exception(
                f"Error occurred while creating ApplicationDecision for OathOfAllegiance ID "
                f"{instance.id}: {str(e)}"
            )

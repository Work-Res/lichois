import logging

from app.models import ApplicationVerification, Application
from app.utils import ApplicationDecisionEnum
from app_decision.models import ApplicationDecision, ApplicationDecisionType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from citizenship.utils import VerificationProcessWhenCompletedIsRequiredForProduction

logger = logging.getLogger(__name__)


@receiver(post_save, sender=ApplicationVerification)
def production_decision_post_save_on_verfication_handler(sender, instance, created, **kwargs):
    if created:
        application = Application.objects.get(
            application_document__document_number=instance.document_number
        )
        if application.application_type in VerificationProcessWhenCompletedIsRequiredForProduction.configured_process():
            try:
                accepted = ApplicationDecisionType.objects.get(
                    code=ApplicationDecisionEnum.ACCEPTED.value
                )
                ApplicationDecision.objects.create(
                    document_number=instance.document_number,
                    final_decision_type=accepted,
                    proposed_decision_type=accepted
                )
                logger.info(f"ApplicationDecision created for verification on completion ID {instance.id}")
            except ObjectDoesNotExist:
                logger.error(f"ApplicationDecisionType with code {ApplicationDecisionEnum.ACCEPTED.value} not found.")
            except Exception as e:
                logger.exception(f"Error occurred while creating ApplicationDecision for ApplicationVerification "
                                 f"{instance.id}: {str(e)}")
        else:
            logger.info(f"Process not met criteria for production creation.")


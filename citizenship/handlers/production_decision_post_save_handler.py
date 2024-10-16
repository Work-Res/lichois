import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import Application, ApplicationDecision
from app_production.handlers.postsave.upload_document_production_handler import (
    UploadDocumentProductionHandler,
)
from citizenship.service.word.intention_by_foreign_spouse import IntentionFSLetterProductionProcess
from citizenship.service.word.intention_by_foreign_spouse.intention_fs_letter_context_generator import (
    IntentionFSContextGenerator,
)
from citizenship.service.word.maturity.maturity_letter_context_generator import (
    MaturityLetterContextGenerator,
)
from citizenship.service.word.maturity.maturity_letter_production_process import (
    MaturityLetterProductionProcess,
)
from citizenship.service.word.registration.registration_context_generator import (
    RegistrationContextGenerator,
)
from citizenship.service.word.registration.registration_letter_production_process import (
    RegistrationLetterProductionProcess,
)
from citizenship.utils import (
    CitizenshipDocumentGenerationIsRequiredForProduction,
    CitizenshipProcessEnum
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=ApplicationDecision)
def production_decision_post_save_handler(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Post-save signal received for new ApplicationDecision instance: {instance.id}")

        try:
            # Fetch the associated application
            logger.debug(f"Attempting to fetch Application with document number: {instance.document_number}")
            application = Application.objects.get(
                application_document__document_number=instance.document_number
            )
            logger.info(f"Fetched Application with ID: {application.id} for ApplicationDecision {instance.id}")

            # Check if document generation is required
            process_name = application.application_type
            logger.debug(f"Checking if document generation is required for application type: {process_name}")

            if (
                    process_name
                    in CitizenshipDocumentGenerationIsRequiredForProduction.configured_process()
            ):
                logger.info(f"Document generation required for application type: {process_name}")

                if application.application_type.lower() == CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value.lower():
                    logger.debug("Using MaturityLetterProductionProcess for decision.")
                    handler = UploadDocumentProductionHandler()
                    context_generator = MaturityLetterContextGenerator()
                    process = MaturityLetterProductionProcess(handler, context_generator)

                elif application.application_type.lower() == CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value.lower():
                    logger.debug("Using IntentionFSLetterProductionProcess for decision.")
                    handler = UploadDocumentProductionHandler()
                    context_generator = IntentionFSContextGenerator()
                    process = IntentionFSLetterProductionProcess(handler, context_generator)

                elif application.application_type.lower() in [
                    CitizenshipProcessEnum.ADOPTED_CHILD_REGISTRATION.value.lower(),
                    CitizenshipProcessEnum.UNDER_20_CITIZENSHIP.value.lower()
                ]:
                    logger.debug("Using RegistrationLetterProductionProcess for decision.")
                    handler = UploadDocumentProductionHandler()
                    context_generator = RegistrationContextGenerator()
                    process = RegistrationLetterProductionProcess(handler, context_generator)

                # Handle the production process for the decision
                logger.info(f"Starting production process for ApplicationDecision {instance.id}")
                process.handle(application, instance)
                logger.info(f"Successfully handled production for ApplicationDecision {instance.id}")

            else:
                logger.info(f"Document generation not required for process: {process_name}")

        except Application.DoesNotExist:
            logger.error(f"Application not found for document number {instance.document_number}")

        except Exception as e:
            logger.error(f"Unexpected error in post-save handler for ApplicationDecision {instance.id}: {e}",
                         exc_info=True)
    else:
        logger.debug(f"Updating, not required for generating an document: {instance.document_number}")

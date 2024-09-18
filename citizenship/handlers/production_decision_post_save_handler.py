import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import Application
from app_decision.models import ApplicationDecision

from app_production.handlers.postsave.upload_document_production_handler import UploadDocumentProductionHandler
from citizenship.service.word.maturity.maturity_letter_context_generator import MaturityLetterContextGenerator
from citizenship.service.word.maturity.maturity_letter_production_process import MaturityLetterProductionProcess
from citizenship.utils import CitizenshipDocumentGenerationIsRequiredForProduction

logger = logging.getLogger(__name__)


@receiver(post_save, sender=ApplicationDecision)
def production_decision_post_save_handler(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Handling post-save for new instance: {instance}")
        try:
            # Fetch the associated application
            application = Application.objects.get(
                application_document__document_number=instance.document_number)

            # Check if document generation is required
            process_name = application.application_type
            if process_name in CitizenshipDocumentGenerationIsRequiredForProduction.configured_process():
                # Use the maturity letter process
                handler = UploadDocumentProductionHandler()
                context_generator = MaturityLetterContextGenerator()
                process = MaturityLetterProductionProcess(handler, context_generator)

                # Handle the production process for the decision
                process.handle(application, instance)

                logger.info(f"Production process handled successfully for {instance}")
            else:
                logger.info(f"Document generation not required for {process_name}")
        except Exception as e:
            logger.error(f"Unexpected error in post-save handler: {e}", exc_info=True)

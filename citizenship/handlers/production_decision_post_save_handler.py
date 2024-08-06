import logging
import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from app_decision.models import ApplicationDecision
from app_production.exceptions.exceptions import ProductionProcessException
from app_production.handlers.common import GenericProductionContext, ProductionConfig
from app_production.handlers.postsave.upload_document_production_handler import UploadDocumentProductionHandler
from citizenship.utils import CitizenshipDocumentGenerationIsRequiredForProduction

logger = logging.getLogger(__name__)


@receiver(post_save, sender=ApplicationDecision)
def production_decision_post_save_handler(sender, instance, created, **kwargs):
    if created:

        logger.info(f"Handling post-save for new instance: {instance}")
        template_path = os.path.join(
            "citizenship", "data", "production", "templates", "maturity_letter_template.docx")
        document_output_path = os.path.join(settings.MEDIA_ROOT, f'{instance.id}.pdf')
        process_name = instance.application_version.application.process_name
        is_required = process_name in CitizenshipDocumentGenerationIsRequiredForProduction.configured_processs
        config = ProductionConfig(
            template_path=template_path,
            document_output_path=document_output_path,
            is_required=is_required
        )

        context = GenericProductionContext()
        document_number = instance.application_version.application.application_document.document_number
        context.context = lambda: {
            'document_type': 'maturity_letter',
            'document_number': document_number
        }
        handler = UploadDocumentProductionHandler()
        try:
            logger.info("Executing document production handler")
            handler.execute(config, context)
            logger.info("Document production handler executed successfully")
        except ProductionProcessException as e:
            logger.error(f"Production process exception: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)

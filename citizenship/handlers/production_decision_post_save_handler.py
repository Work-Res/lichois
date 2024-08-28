import logging
import os

from datetime import datetime
from dateutil.relativedelta import relativedelta

from datetime import date

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from app.models import Application
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
        document_output_path = os.path.join(settings.MEDIA_ROOT, f'{instance.id}.docx')

        application = Application.objects.get(application_document__document_number=instance.document_number)
        process_name = application.application_type

        is_required = process_name in CitizenshipDocumentGenerationIsRequiredForProduction.configured_process()
        if is_required:
            config = ProductionConfig(
                template_path=template_path,
                document_output_path=document_output_path,
                is_required=is_required
            )

            context = GenericProductionContext()
            document_number = instance.document_number
            years  = datetime.now()+relativedelta(months=30)
            context.context = lambda: {
                'document_type': 'maturity_letter',
                'document_number': document_number,
                'reference_number': document_number,
                'today_date': date.today().strftime("%Y-%m-%d"),
                'applicant_fullname': 'Test test',
                'salutation': 'Sir/Madam',
                'end_date': years.strftime("%Y-%m-%d"),
                'start_date': datetime.now().strftime("%Y-%m-%d"),
                'officer_fullname': 'Ana Mokgethi',
                'position': 'Minister',
                'officer_contact_information': '',
                'applicant_address': 'P O BOX 300, Gaborone'
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

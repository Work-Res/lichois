import os
import logging
from django.conf import settings
from datetime import date

from app_production.handlers.common import ProductionConfig
from app_production.handlers.postsave.upload_document_production_handler import UploadDocumentProductionHandler
from citizenship.service.word.maturity.maturity_letter_context_generator import MaturityLetterContextGenerator


class ProductionProcess:
    def handle(self, application, decision):
        raise NotImplementedError("Subclasses must implement 'handle' method")


class MaturityLetterProductionProcess(ProductionProcess):
    def __init__(self, handler: UploadDocumentProductionHandler, context_generator: MaturityLetterContextGenerator):
        self.handler = handler
        self.logger = logging.getLogger(__name__)
        self.context_generator = context_generator

    def handle(self, application, decision):
        status = decision.final_decision_type.code
        date_string = date.today().strftime("%Y-%m-%d")
        template_path = os.path.join(
            "citizenship", "data", "production", "templates", f"maturity_letter_{status}_template.docx")
        document_output_path = os.path.join(
            settings.MEDIA_ROOT, f'maturity_letter_{application.document_number}_{date_string}.docx')

        config = ProductionConfig(
            template_path=template_path,
            document_output_path=document_output_path,
            is_required=True
        )
        context = self.context_generator.generate(application)

        try:
            self.handler.execute(config, context)
        except Exception as e:
            self.logger.error(f"Error in handling production process: {str(e)}", exc_info=True)

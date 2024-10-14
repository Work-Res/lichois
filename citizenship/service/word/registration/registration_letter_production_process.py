import os
import logging
from django.conf import settings
from datetime import date

from app_production.handlers.common import ProductionConfig, GenericProductionContext
from app_production.handlers.postsave.upload_document_production_handler import UploadDocumentProductionHandler
from citizenship.service.word.maturity.maturity_letter_context_generator import MaturityLetterContextGenerator


class ProductionProcess:
    def handle(self, application, decision):
        raise NotImplementedError("Subclasses must implement 'handle' method")


class RegistrationLetterProductionProcess(ProductionProcess):
    def __init__(self, handler: UploadDocumentProductionHandler, context_generator: MaturityLetterContextGenerator):
        self.handler = handler
        self.logger = logging.getLogger(__name__)
        self.context_generator = context_generator

    def handle(self, application, decision):
        status = decision.proposed_decision_type.code.lower()
        date_string = date.today().strftime("%Y-%m-%d")
        template_path = os.path.join(
            "citizenship", "data", "production", "templates", f"indosement_{status}_template.docx")
        document_output_path = os.path.join(
            settings.MEDIA_ROOT, f'indosement_{application.application_document.document_number}_{date_string}_{status}.docx')

        config = ProductionConfig(
            template_path=template_path,
            document_output_path=document_output_path,
            is_required=True
        )

        self.logger.debug(f"Generated template path: {template_path}")
        self.logger.debug(f"Generated document output path: {document_output_path}")
        self.logger.info(
            f"Starting production process for application {application.id} and decision {decision.id} "
            f"with status '{status}'"
        )

        try:
            # Generate context for the production process
            self.logger.debug("Generating context for production...")
            context = self.context_generator.generate(application)
            generic_context = GenericProductionContext()
            generic_context.context = lambda: context
            self.logger.debug(f"Generated context: {context}")

            # Execute the handler with the configuration and context
            self.logger.info(
                f"Executing production handler with config template '{template_path}' "
                f"and output '{document_output_path}'"
            )
            self.handler.execute(config, generic_context)

            self.logger.info(
                f"Production process completed successfully for application {application.id}, "
                f"decision {decision.id}"
            )
        except FileNotFoundError as e:
            # Specific error logging for missing template files
            self.logger.error(
                f"Template file not found at '{template_path}' for application {application.id}, "
                f"decision {decision.id}: {str(e)}",
                exc_info=True
            )
        except Exception as e:
            # Generic error logging for unexpected exceptions
            self.logger.error(
                f"An error occurred during the production process for application {application.id}, "
                f"decision {decision.id}: {str(e)}",
                exc_info=True
            )

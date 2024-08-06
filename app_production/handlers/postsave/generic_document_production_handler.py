import logging

from app_production.exceptions.exceptions import ProductionProcessException
from app_production.handlers.common import ProductionHandler, ProductionConfig, GenericProductionContext
from app_production.services.document import WordDocumentTemplateService


class GenericDocumentProductionHandler(ProductionHandler[ProductionConfig, GenericProductionContext]):

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def execute(self, config_cls: ProductionConfig, production_context: GenericProductionContext) -> None:
        self.logger.info("Starting document production")
        self.logger.debug(f"Config class: {config_cls}")
        self.logger.debug(f"Production context: {production_context}")

        try:
            self.logger.debug(f"Loading template from path: {config_cls.template_path}")
            document = WordDocumentTemplateService(template_path=config_cls.template_path)

            self.logger.debug(f"Replacing placeholders with context: {production_context.context()}")
            document.replace_placeholders(context=production_context.context())
            document.save_document(document, config_cls.document_output_path)
            self.logger.info("Document production completed successfully")
        except FileNotFoundError as e:
            self.logger.error(f"Template file not found: {e}")
            raise ProductionProcessException(f"Template file not found: {e}")
        except Exception as e:
            self.logger.error(f"Error during production: {e}")
            raise ProductionProcessException(f"Error during production: {e}")

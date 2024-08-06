import os

from django.core.files.base import ContentFile
from app_production.exceptions.exceptions import ProductionProcessException
from app_production.handlers.common import ProductionConfig, GenericProductionContext
from app_production.handlers.postsave.generic_document_production_handler import GenericDocumentProductionHandler
from app_production.models import ProductionAttachmentDocument


class UploadDocumentProductionHandler(GenericDocumentProductionHandler):

    def execute(self, config_cls: ProductionConfig, production_context: GenericProductionContext) -> None:
        self.logger.info("Starting document production and upload")
        if config_cls.is_required:
            super().execute(config_cls, production_context)

            try:
                self.logger.debug(f"Reading document from path: {config_cls.document_output_path}")
                with open(config_cls.document_output_path, 'rb') as file:
                    document_content = file.read()

                document_name = os.path.basename(config_cls.document_output_path)
                content_file = ContentFile(document_content, document_name)

                # Create and save ProductionAttachmentDocument
                attachment_document = ProductionAttachmentDocument(
                    document_type=production_context.context().get('document_type'),
                    document_number=production_context.context().get('document_number'),
                    pdf_document=content_file
                )
                attachment_document.save()

                self.logger.info("Document production and upload completed successfully")
            except Exception as e:
                self.logger.error(f"Error during document upload: {e}")
                raise ProductionProcessException(f"Error during document upload: {e}")

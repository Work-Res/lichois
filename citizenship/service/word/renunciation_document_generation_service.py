import logging
import os.path
import os
import tempfile
from django.core.files.base import ContentFile

from datetime import date

from . import RenunciationDataGenerator
from ...exception.interview_score_sheet_error import (
    PDFConversionError,
    WordDocumentCreationError,
)

from .score_sheet_document_generator_service import ScoresheetDocumentGeneratorService
from .data_generator import DataGeneratorException
from ...models.renunciation import RenunciationAttachment

logger = logging.getLogger(__name__)


class RenunciationDocumentGenerationService:

    def __init__(
        self,
        data_generator_class=RenunciationDataGenerator,
        doc_generator_class=ScoresheetDocumentGeneratorService,
    ):
        self.data_generator_class = data_generator_class
        self.doc_generator_class = doc_generator_class

    def generate_document(self, document_number):
        logger.info(f"Handling document generation for renunciation {document_number}")
        template_path = os.path.join("citizenship", "data", "production", "templates",
                                     "renunciation_letter_template.docx")

        try:
            # Generate the context required for document creation
            context = self.data_generator_class(document_number=document_number).context()
            today_str = date.today().strftime("%Y-%m-%d")

            # Create a temporary directory to store the generated files
            with tempfile.TemporaryDirectory() as temp_dir:
                word_path = f"{temp_dir}/renunciation_{today_str}_{document_number}.docx"
                pdf_path = f"{temp_dir}/renunciation_{today_str}_{document_number}.pdf"

                # Create the document service that generates Word and PDF
                service = self.doc_generator_class([], word_path, pdf_path, template_path=template_path,
                                                   context=context)
                service.create_and_convert()

                # Prepare RenunciationAttachment model to store the generated document
                attachment = RenunciationAttachment()
                attachment.document_number = document_number

                # Save the Word document
                with open(word_path, 'rb') as word_file:
                    attachment.document.save(f"renunciation_{document_number}.docx", ContentFile(word_file.read()))

                # Save the RenunciationAttachment record
                attachment.save()

                logger.info(f"PDF and DOCX documents created and saved for renunciation {document_number}")

                return attachment  # Optionally return the attachment object for further use

        except (WordDocumentCreationError, PDFConversionError, DataGeneratorException) as e:
            logger.error(f"Error during document creation for renunciation {document_number}: {e}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error creating documents for renunciation {document_number}: {e}")
            raise

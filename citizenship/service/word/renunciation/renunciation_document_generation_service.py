import logging
import os.path
import os
import tempfile

from datetime import date
from django.core.files.base import ContentFile

from citizenship.exception.interview_score_sheet_error import (
    PDFConversionError,
    WordDocumentCreationError,
)
from citizenship.service.word.renunciation import RenunciationContextDataGenerator

from citizenship.service.word.score_sheet_document_generator_service import ScoresheetDocumentGeneratorService
from citizenship.service.word.data_generator import DataGeneratorException
from citizenship.models.renunciation import RenunciationAttachment
from citizenship.utils import CitizenshipProcessEnum

logger = logging.getLogger(__name__)


class RenunciationDocumentGenerationService:

    def __init__(
        self,
        data_generator_class=RenunciationContextDataGenerator,
        doc_generator_class=ScoresheetDocumentGeneratorService,
    ):
        self.data_generator_class = data_generator_class
        self.doc_generator_class = doc_generator_class

    def handle(self, application):
        # Early exit if application type doesn't match
        if application.application_type.lower() != CitizenshipProcessEnum.RENUNCIATION.value.lower():
            return

        document_number = application.application_document.document_number
        logger.info(f"Handling document generation for renunciation {document_number}")

        template_path = os.path.join(
            "citizenship", "data", "production", "templates", "renunciation_letter_template.docx"
        )

        try:
            # Generate the context for the renunciation document
            context = self.context_generator.generate(application)
            today_str = date.today().strftime("%Y-%m-%d")

            with tempfile.TemporaryDirectory() as temp_dir:
                word_path, pdf_path = self._generate_file_paths(temp_dir, document_number, today_str)

                # Create and convert the document
                self._create_and_convert_documents(word_path, pdf_path, template_path, context)

                # Save the documents in the RenunciationAttachment model
                attachment = self._save_attachment(document_number, word_path)

                logger.info(f"PDF and DOCX documents created and saved for renunciation {document_number}")
                return attachment  # Return the saved attachment

        except (WordDocumentCreationError, PDFConversionError, DataGeneratorException) as e:
            logger.error(f"Document creation failed for renunciation {document_number}: {e}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error while creating documents for renunciation {document_number}: {e}")
            raise

    def _generate_file_paths(self, temp_dir, document_number, today_str):
        """
        Generate paths for the temporary Word and PDF files.
        """
        word_path = os.path.join(temp_dir, f"renunciation_{today_str}_{document_number}.docx")
        pdf_path = os.path.join(temp_dir, f"renunciation_{today_str}_{document_number}.pdf")
        return word_path, pdf_path

    def _create_and_convert_documents(self, word_path, pdf_path, template_path, context):
        """
        Create Word and PDF documents from the template.
        """
        service = self.doc_generator_class([], word_path, pdf_path, template_path=template_path, context=context)
        service.create_and_convert()

    def _save_attachment(self, document_number, word_path):
        """
        Save the Word document in the RenunciationAttachment model.
        """
        attachment = RenunciationAttachment(document_number=document_number)

        # Save the Word document
        with open(word_path, 'rb') as word_file:
            attachment.document.save(f"renunciation_{document_number}.docx", ContentFile(word_file.read()))

        # Save the attachment record in the database
        attachment.save()

        return attachment

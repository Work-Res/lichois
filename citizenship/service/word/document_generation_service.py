import logging
import tempfile

from . import DataGenerator
from ...exception.interview_score_sheet_error import (
    PDFConversionError,
    WordDocumentCreationError,
)

from .score_sheet_document_generator_service import ScoresheetDocumentGeneratorService
from .data_generator import DataGeneratorException

logger = logging.getLogger(__name__)


class DocumentGenerationService:

    def __init__(
        self,
        data_generator_class=DataGenerator,
        doc_generator_class=ScoresheetDocumentGeneratorService,
    ):
        self.data_generator_class = data_generator_class
        self.doc_generator_class = doc_generator_class

    def generate_scoresheet_document(self, scoresheet):
        logger.info(f"Handling document generation for scoresheet {scoresheet.id}")
        try:
            data = self.data_generator_class(scoresheet).generate_data()

            with tempfile.TemporaryDirectory() as temp_dir:
                word_path = f"{temp_dir}/scoresheet_{scoresheet.id}.docx"
                pdf_path = f"{temp_dir}/scoresheet_{scoresheet.id}.pdf"

                service = self.doc_generator_class(data, word_path, pdf_path)
                service.create_and_convert()

                scoresheet.document = pdf_path
                scoresheet.save()

                logger.info(
                    f"PDF document created for scoresheet {scoresheet.id} at {pdf_path}"
                )
        except (
            WordDocumentCreationError,
            PDFConversionError,
            DataGeneratorException,
        ) as e:
            logger.error(
                f"Error during document creation for scoresheet {scoresheet.id}: {e}"
            )
            raise
        except Exception as e:
            logger.exception(
                f"Unexpected error creating PDF for scoresheet {scoresheet.id}: {e}"
            )
            raise

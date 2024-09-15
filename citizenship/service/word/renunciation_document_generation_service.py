import logging
import os.path
import tempfile

from datetime import datetime

from . import DataGenerator
from ...exception.interview_score_sheet_error import (
    PDFConversionError,
    WordDocumentCreationError,
)

from .score_sheet_document_generator_service import ScoresheetDocumentGeneratorService
from .data_generator import DataGeneratorException

logger = logging.getLogger(__name__)


class RenunciationDocumentGenerationService:

    def __init__(
        self,
        data_generator_class=DataGenerator,
        doc_generator_class=ScoresheetDocumentGeneratorService,
    ):
        self.data_generator_class = data_generator_class
        self.doc_generator_class = doc_generator_class

    def generate_scoresheet_document(self, scoresheet):
        logger.info(f"Handling document generation for scoresheet {scoresheet.id}")
        template_path = os.path.join("citizenship", "data", "production", "templates", "score_sheet_template.docx")
        try:
            context = {}
            today = datetime.now()
            context.update({
                "reference_number": scoresheet.interview.application.application_document.document_number,
                "today_date": today.strftime("%Y-%m-%d")
            })
            data = self.data_generator_class(scoresheet).generate_data()
            with tempfile.TemporaryDirectory() as temp_dir:
                word_path = f"{temp_dir}/scoresheet_{scoresheet.id}.docx"
                pdf_path = f"{temp_dir}/scoresheet_{scoresheet.id}.pdf"

                service = self.doc_generator_class(data, word_path, pdf_path, template_path=template_path,
                                                   context=context)
                service.create_and_convert()

                scoresheet.document = word_path
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

import logging
from docx import Document
from docx2pdf import convert

from citizenship.exception.interview_score_sheet_error import WordDocumentCreationError, PDFConversionError

logger = logging.getLogger(__name__)


class ScoresheetDocumentGeneratorService:
    def __init__(self, data, word_path, pdf_path):
        """
        Initialize the service with data and paths.

        Args:
            data (list): The data to populate the table.
            word_path (str): The path to save the Word document.
            pdf_path (str): The path to save the PDF document.
        """
        self.data = data
        self.word_path = word_path
        self.pdf_path = pdf_path

    def create_word_document(self):
        """
        Create a Word document with the provided data.
        """
        try:
            # Create a new Document
            doc = Document()

            # Add a title
            doc.add_heading('Interview Score Sheet', level=1)

            # Add a table
            table = doc.add_table(rows=len(self.data), cols=4)
            table.style = 'Table Grid'

            # Populate the table
            for row_idx, row_data in enumerate(self.data):
                row = table.rows[row_idx]
                for col_idx, cell_data in enumerate(row_data):
                    cell = row.cells[col_idx]
                    cell.text = cell_data

            # Style the header row
            hdr_cells = table.rows[0].cells
            for cell in hdr_cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.bold = True

            # Save the document
            doc.save(self.word_path)
            logger.info(f"Word document created at {self.word_path}")
        except Exception as e:
            logger.exception(f"Error creating Word document: {e}")
            raise WordDocumentCreationError(f"Error creating Word document: {e}")

    def convert_to_pdf(self):
        """
        Convert the Word document to PDF.
        """
        try:
            # Convert the Word document to PDF
            convert(self.word_path, self.pdf_path)
            logger.info(f"PDF document created at {self.pdf_path}")
        except Exception as e:
            logger.exception(f"Error converting Word document to PDF: {e}")
            raise PDFConversionError(f"Error converting Word document to PDF: {e}")

    def create_and_convert(self):
        """
        Create the Word document and convert it to PDF.
        """
        self.create_word_document()
        self.convert_to_pdf()

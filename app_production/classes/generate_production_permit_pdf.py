import logging

from .permit_data_processor import PermitDataProcessor
from app_pdf_utilities.classes import ConvertHtmlToPdf

from typing import Optional


class GenerateProductionPermitPDF:
    """Generates the production permit PDF and saves it in the specified location."""

    def __init__(
        self,
        document_number: str,
        file_location: Optional[str] = None,
        configuration_file_name=None,
    ):
        """
        Initialize the class with document number and optional file location.

        :param document_number: The document number for the permit.
        :param file_location: The location where the PDF should be saved (default: None).
        """
        self.logger = logging.getLogger(__name__)

        self.document_number = document_number
        self.file_location = file_location
        self.data_processor = PermitDataProcessor(
            document_number=document_number,
            configuration_file_name=configuration_file_name,
        )
        self.pdf_generator = ConvertHtmlToPdf()

    def generate_pdf(self) -> None:
        """Generate the PDF for the production permit."""
        try:
            # Transform data
            self.logger.info(
                f"Starting data transformation for document number {self.document_number}."
            )
            prepared_data = self.data_processor.transform_data()
            self.logger.info(
                f"Data transformation completed for document number {self.document_number}."
            )

            # Generate PDF
            self.logger.info(
                f"Starting PDF generation for document number {self.document_number}."
            )
            pdf_data = self.pdf_generator.convert_html_to_pdf(
                context=prepared_data,
                file_location=self.file_location,
                template_path="pdf/work-permit.html",
            )
            self.logger.info(
                f"PDF generation completed. File saved to {self.file_location}."
            )
            return pdf_data

        except Exception as e:
            print(f"Error occurred {e}")
            self.logger.error(f"An error occurred while generating the PDF: {e}")
            raise

    def create_or_update_permit(self, pdf):
        pass

import logging

from datetime import date, datetime

from app.models import Application
from app_production.handlers.common import GenericProductionContext


class DataGeneratorException(Exception):
    pass


logger = logging.getLogger(__name__)


class RenunciationDataGenerator:
    def __init__(self, document_number):
        self.document_number = document_number

    def context(self):
        generic_production = GenericProductionContext()
        generic_production.context = lambda: self.prepare_context()
        return generic_production

    def prepare_context(self):
        app = self._application()

        context = {
            'document_type': 'maturity_letter',
            'document_number': self.document_number,
            'reference_number': self.document_number,
            'certificate_number': '',
            'today_date': date.today().strftime("%Y-%m-%d"),
            'applicant_fullname': 'Test test',
            'salutation': 'Sir/Madam',
            'citizenship_end_date': '',
            'citizenship_start_date': datetime.now().strftime("%Y-%m-%d"),
            'officer_fullname': 'Ana Mokgethi',
            'position': 'Minister',
            'officer_contact_information': '',
            'applicant_address': 'P O BOX 300, Gaborone'
        }
        return context

    def _application(self):
        try:
            return Application.objects.get(
                application_document__document_number=self.document_number
            )
        except Application.DoesNotExist:
            pass

    def generate_data(self):
        """Generates the data based on the scoresheet's aggregated information."""
        try:
            # Initialize data with headers
            data = [("Category", "Marks", "Marks Scored", "Comments")]

            # Parse the aggregated data
            aggregated_data_list = self.parse_aggregated_data()

            # Append the data from aggregated data
            data.extend(
                (item.get("text", "Unknown"),
                 item.get("marks_range", "N/A"),
                 item.get("average_score", "N/A"),
                 "NA")
                for item in aggregated_data_list
            )

            logger.info(f"Successfully generated data for scoresheet {self.scoresheet.id}")
            return data

        except DataGeneratorException as e:
            logger.exception(f"Data generation failed for scoresheet {self.scoresheet.id}: {e}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error during data generation for scoresheet {self.scoresheet.id}: {e}")
            raise DataGeneratorException(
                f"Unexpected error during data generation for scoresheet {self.scoresheet.id}: {e}")

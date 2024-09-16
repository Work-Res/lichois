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
            'document_type': 'renunciation_letter',
            'document_number': self.document_number,
            'reference_number': self.document_number,
            'certificate_number': '',
            'today_date': date.today().strftime("%Y-%m-%d"),
            'applicant_fullname': app.full_name() if app else '',
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
            return None

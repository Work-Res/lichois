import logging

from datetime import date, datetime

from app_address.models import ApplicationAddress
from app_production.handlers.common import GenericProductionContext
from citizenship.service.word.maturity import DocumentContextGenerator


class DataGeneratorException(Exception):
    pass


logger = logging.getLogger(__name__)


class RenunciationContextDataGenerator(DocumentContextGenerator):

    def generate(self,  application):
        document_number = application.application_document.document_number
        context = {
            'document_type': 'renunciation_letter',
            'document_number': document_number,
            'reference_number': document_number,
            'certificate_number': '',
            'today_date': date.today().strftime("%Y-%m-%d"),
            'applicant_fullname': application.full_name() if application else '',
            'salutation': 'Sir/Madam',
            'citizenship_end_date': '',
            'citizenship_start_date': datetime.now().strftime("%Y-%m-%d"),
            'officer_fullname': 'Ana Mokgethi',
            'position': 'Minister',
            'officer_contact_information': '',
            'applicant_address': self.applicant_address(application)
        }
        return context

    def applicant_address(self, application):
        try:
            # Use select_related to optimize the query by fetching related objects in one go
            application_address = ApplicationAddress.objects.select_related('country').get(
                document_number=application.application_document.document_number
            )

            # Format the address components
            address_parts = [
                application_address.private_bag or '',
                application_address.po_box or '',
                application_address.street_address or '',
                # application_address.country.code if application_address.country else ''
            ]

            # Join the non-empty parts with proper spacing
            full_address = ' '.join(part for part in address_parts if part)

            return full_address or 'Address not available'

        except ApplicationAddress.DoesNotExist:
            # Handle case where the address is not found
            return 'Address not available'

import logging

from app_address.models import ApplicationAddress
from django.core.exceptions import MultipleObjectsReturned
from app_personal_details.models import Person


logger = logging.getLogger(__name__)


class PrepareGazetteForDownload:

    def __init__(self, batch_applications, address_type=None):
        self.batch_applications = batch_applications
        self.address_type = address_type or 'residential'
        self.data = []

    def get_application_address(self, application):
        try:
            return ApplicationAddress.objects.get(
                document_number=application.application_document.document_number,
                address_type=self.address_type
            )
        except MultipleObjectsReturned:
            logger.warning(f"Multiple addresses found for application {application.id} with "
                           f"address type {self.address_type}. Returning the first one.")
            return ApplicationAddress.objects.filter(
                document_number=application.application_document.document_number,
                address_type=self.address_type
            ).first()
        except ApplicationAddress.DoesNotExist:
            logger.error(f"No address found for application {application.id} with address type {self.address_type}.")
            return None

    def get_personal_details(self, application):
        try:
            return Person.objects.get(
                document_number=application.application_document.document_number
            )
        except Person.DoesNotExist:
            logger.error(f"No personal details found for application {application.application_document.document_number}.")
            return None
        except MultipleObjectsReturned:
            logger.warning(f"Multiple personal details found for application {application.application_document.document_number}. Returning the first one.")
            return Person.objects.filter(
                application_version__application=application
            ).first()

    def prepared_data(self):
        header_row = ["ID", "Fullname", "Location", "Document Number"]
        self.data.append(header_row)

        for index, batch_application in enumerate(self.batch_applications):
            try:
                address = self.get_application_address(batch_application.application)
                person_details = self.get_personal_details(batch_application.application)

                if not address or not person_details:
                    logger.error(f"Missing data for application {batch_application.application.id}. Skipping...")
                    continue

                row_content = [
                    index,
                    person_details.full_name(),
                    self.applicant_address(batch_application.application),
                    batch_application.application.application_document.document_number
                ]
                self.data.append(row_content)
            except AttributeError as e:
                # Handle missing attributes or None values
                logger.error(f"AttributeError: {e} for application {index}.")
            except Exception as e:
                # Handle any other exceptions that may occur
                logger.error(f"Unexpected error: {e} for application {index}.")

        return self.data

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
                # application_address.street_address or '',
                application_address.district.get("code") if application_address.district else '',
                application_address.village.get("code") if application_address.village else ''
                # application_address.country.code if application_address.country else ''
            ]

            # Join the non-empty parts with proper spacing
            full_address = ' '.join(part for part in address_parts if part)

            return full_address or 'Address not available'
        except ApplicationAddress.DoesNotExist:
            # Handle case where the address is not found
            return 'Address not available'

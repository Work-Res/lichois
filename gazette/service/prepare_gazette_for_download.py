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
                application_version__application=application,
                address_type=self.address_type
            )
        except MultipleObjectsReturned:
            logger.warning(f"Multiple addresses found for application {application.id} with "
                           f"address type {self.address_type}. Returning the first one.")
            return ApplicationAddress.objects.filter(
                application_version__application=application,
                address_type=self.address_type
            ).first()
        except ApplicationAddress.DoesNotExist:
            logger.error(f"No address found for application {application.id} with address type {self.address_type}.")
            return None

    def get_personal_details(self, application):
        try:
            return Person.objects.get(
                application_version__application=application
            )
        except Person.DoesNotExist:
            logger.error(f"No personal details found for application {application.id}.")
            return None
        except MultipleObjectsReturned:
            logger.warning(f"Multiple personal details found for application {application.id}. Returning the first one.")
            return Person.objects.filter(
                application_version__application=application
            ).first()

    def prepared_data(self):
        header_row = ["ID", "Fullname", "Location", "Document Number"]
        self.data.append(header_row)

        for index, application in enumerate(self.batch_applications):
            try:
                address = self.get_application_address(application)
                person_details = self.get_personal_details(application)

                if not address or not person_details:
                    logger.error(f"Missing data for application {application.id}. Skipping...")
                    continue

                row_content = [
                    index,
                    person_details.full_name(),
                    address.city,
                    application.application_document.document_number
                ]
                self.data.append(row_content)
            except AttributeError as e:
                # Handle missing attributes or None values
                logger.error(f"AttributeError: {e} for application {index}.")
            except Exception as e:
                # Handle any other exceptions that may occur
                logger.error(f"Unexpected error: {e} for application {index}.")

        return self.data

import logging
from django.core.exceptions import ObjectDoesNotExist

from app_address.models import ApplicationAddress
from app_contact.models import ApplicationContact
from app_personal_details.models import Person


class ApplicantPaymentDetailsService:
    """
    Class to retrieve and prepare an applicant's personal and contact details.
    """

    def __init__(self, document_number):
        self.document_number = document_number
        self.logger = logging.getLogger(__name__)

    def get_details(self):
        """
        Retrieves the applicant's personal and contact details.
        """
        try:
            person = self._get_person()
            # contact = self._get_contact()

            address = self._get_address()
            address_parts = [
                address.private_bag or '',
                address.po_box or '',
                address.street_address or '',
                # application_address.country.code if application_address.country else ''
            ]
            # Join the non-empty parts with proper spacing
            full_address = ' '.join(part for part in address_parts if part)

            self.logger.info("Successfully retrieved applicant details for document number: %s", self.document_number)

            return {
                'bill_to_forename': person.first_name,
                'bill_to_surname': person.last_name,
                'bill_to_email': 'tsetsiba@gmail.com',
                'bill_to_address_line1': full_address,
                'bill_to_address_city': 'Gaborone',  # address.city,
                'bill_to_address_postal_code': '0000',
                'bill_to_address_country': 'BW',
                'bill_to_address_state': 'Central'  # TODO what to set here?
            }

        except ObjectDoesNotExist as e:
            self.logger.error("Error retrieving applicant details: %s", e)
            raise ValueError(f"Unable to retrieve details for document number: {self.document_number}") from e
        except Exception as e:
            self.logger.error("Unexpected error occurred: %s", e)
            raise RuntimeError("An unexpected error occurred while retrieving applicant details.") from e

    def _get_person(self):
        """
        Retrieves the applicant's personal details.
        """
        try:
            person = Person.objects.get(
                document_number=self.document_number,
                person_type='applicant'
            )
            self.logger.debug("Successfully retrieved person details for document number: %s", self.document_number)
            return person
        except Person.DoesNotExist:
            self.logger.warning("No person found for document number: %s", self.document_number)
            raise
        except Exception as e:
            self.logger.error("Unexpected error retrieving person: %s", e)
            raise

    def _get_contact(self):
        """
        Retrieves the applicant's contact details.
        """
        try:
            contact = ApplicationContact.objects.get(contact_type="EMAIL")
            self.logger.debug("Successfully retrieved address details for document number: %s", self.document_number)
            return contact
        except ApplicationContact.DoesNotExist:
            self.logger.warning("No contact found of type 'EMAIL' for document number: %s", self.document_number)
            raise
        except Exception as e:
            self.logger.error("Unexpected error retrieving contact: %s", e)
            raise

    def _get_address(self):
        """
        Retrieves the applicant's address details.
        """
        try:
            address = ApplicationAddress.objects.get(document_number=self.document_number,
                                                     person_type='applicant')
            self.logger.debug("Successfully retrieved address details for document number: %s", self.document_number)
            return address
        except ApplicationAddress.DoesNotExist:
            self.logger.warning("No contact found of type 'EMAIL' for document number: %s", self.document_number)
            raise
        except Exception as e:
            self.logger.error("Unexpected error retrieving contact: %s", e)
            raise

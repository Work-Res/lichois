import logging

from .data_helper import DataHelper
from typing import Union

from app_personal_details.models import Person, Passport, Permit
from app_address.models import ApplicationAddress
from app_attachments.models import ApplicationAttachment
from app.models import ApplicationDocument

from workresidentpermit.models import WorkPermit


class DataProcessorWorkPermit(DataHelper):
    """
        The class is responsible for processing or preparing data in some way.
    """

    logger = logging.getLogger(__name__)

    def application_document(self, document_number: str) -> Union[ApplicationDocument, None]:
        try:
            if not document_number:
                raise ValueError("Document number cannot be empty")
            # Retrieve the person if exists
            application_document = ApplicationDocument.objects.get(document_number=document_number)
            return application_document
        except ApplicationDocument.DoesNotExist:
            # Log the error
            self.logger.error(f"Application document with document number '{document_number}' does not exist")
            return None

    def personal_details(self, document_number: str) -> Union[Person, None]:
        try:
            if not document_number:
                raise ValueError("Document number cannot be empty")
            # Retrieve the person if exists
            person = Person.objects.get(document_number=document_number)
            return person
        except Person.DoesNotExist:
            # Log the error
            self.logger.error(f"Person with document number '{document_number}' does not exist")
            return None

    def passport(self, document_number) -> Union[Passport, None]:
        try:
            if not document_number:
                raise ValueError("Document number cannot be empty")
            # Retrieve the person if exists
            person = Passport.objects.get(document_number=document_number)
            return person
        except Passport.DoesNotExist:
            # Log the error
            self.logger.error(f"Passport with document number '{document_number}' does not exist")
            return None

    def permit(self, document_number) -> Union[Permit, None]:
        try:
            if not document_number:
                raise ValueError("Document number cannot be empty")
            # Retrieve the person if exists
            permit = Permit.objects.get(document_number=document_number)
            return permit
        except Permit.DoesNotExist:
            # Log the error
            self.logger.error(f"Permit with document number '{document_number}' does not exist")
            return None

    def address(self, document_number):
        try:
            if not document_number:
                raise ValueError("Document number cannot be empty")

            address = ApplicationAddress.objects.get(document_number=document_number)
            return address
        except ApplicationAddress.DoesNotExist:
            self.logger.error(f"Application address with document number '{document_number}' does not exist")

    def contacts(self, document_number=None):
        pass

    def passport_photo(self, document_number) -> Union[ApplicationAttachment, None]:
        try:
            if not document_number:
                raise ValueError("Document number cannot be empty")
            attachment = ApplicationAttachment.objects.get(
                document_number=self.document_number, document_type__code="PASSPORT_PHOTO")
            return attachment
        except ApplicationAttachment.DoesNotExist:
            self.logger.error(f"Application attachment with document number '{document_number}' does not exist")
        return attachment

    def work_permit(self, document_number=None) -> Union[WorkPermit, None]:
        try:
            if not document_number:
                raise ValueError("Document number cannot be empty")

            work_permit = WorkPermit.objects.get(document_number=document_number)
            return work_permit
        except WorkPermit.DoesNotExist:
            self.logger.error(f"WorkPermit with document number '{document_number}' does not exist")

    def transform_data(self, document_number):
        """  List of required permit fields
                data.permit_number
                data.place_of_issue
                data.valid_from
                data.surname <<
                data.full_name
                data.passport_number
                data.gender
                data.date_of_birth
                data.country_cso
                data.security_code
            :return: data
        """
        personal_details = self.personal_details(document_number)
        passport = self.passport(document_number)
        permit = self.permit(document_number)
        application_document = self.application_document(document_number)
        applicant = application_document.applicant if application_document else None

        self.add_field(field_name="surname", field_value=self.set_field_value(personal_details, "first_name"))
        self.add_field(field_name="full_name", field_value=personal_details.full_name())
        self.add_field(field_name="passport_number", field_value=self.set_field_value(passport, "passport_number"))
        self.add_field(field_name="gender", field_value=self.set_field_value(personal_details, "gender"))
        self.add_field(field_name="date_of_birth", field_value=self.set_field_value(personal_details, "dob"))
        self.add_field(field_name="place_of_issue", field_value=self.set_field_value(permit, "place_issue"))
        self.add_field(field_name="permit_number", field_value=self.set_field_value(permit, "permit_no"))
        self.add_field(field_name="valid_from", field_value=self.set_field_value(permit, "date_issued"))
        self.add_field(field_name="valid_to", field_value=self.set_field_value(permit, "date_expiry"))
        self.add_field(field_name="country_cso", field_value=self.set_field_value(applicant, "country_cso"))
        self.add_field(field_name="permit_type", field_value=self.set_field_value(permit, "permit_type"))
        return self.data


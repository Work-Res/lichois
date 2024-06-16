import os

from django.test import TestCase
from datetime import date

from unittest.mock import patch

from ..validators import ResidentPermitValidator

from app.models import Application, ApplicationDocument, ApplicationStatus, ApplicationUser
from app_personal_details.models import Person, Passport
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact
from app_checklist.classes import CreateChecklistService
from app_checklist.models import ClassifierItem
from app_attachments.models import ApplicationAttachment, AttachmentDocumentType
from app.utils import ApplicationStatusEnum
from workresidentpermit.models import ResidencePermit

from faker import Faker


def application(status):
    try:
        obj = Application.objects.get(application_status__status=status)
        return obj
    except Application.DoesNotExist:
        return None


class TestResidentPermitValidator(TestCase):

    def create_data(self):
        file_name = "attachment_documents.json"
        output_file = os.path.join(os.getcwd(), "app_checklist", "data", file_name)
        create = CreateChecklistService()
        create.create(file_location=output_file)

        applicant = ApplicationUser(
            full_name="Test test",
            user_identifier="YYYXXX",
            work_location_code="01",
            dob="2000106")
        application_document = ApplicationDocument(
            id="abc",
            applicant=applicant,
            document_number="WR0001200202",
            signed_date=date.today(),
            submission_customer="test"
        )
        status = ApplicationStatus(id="abcd", code="NEW")
        app = Application(
            id="yze",
            last_application_version_id=1,
            application_document=application_document,
            application_status=status,
            process_name="WORK_RESIDENT_PERMIT"
        )
        return app

    @classmethod
    def setUpTestData(cls):
        pass

    def test_validate_when_is_false(self):
        """Test WorkPermitValidator.validate when all required that not provided.
        """
        validator = ResidentPermitValidator(
           process=None,
           work_resident_permit=None,
           document_number=None)
        self.assertFalse(validator.is_valid())
        self.assertGreater(len(validator.response.messages), 1)
        self.assertEqual(len(validator.response.messages), 7)

    @patch('app.models.Application.objects.get')
    def test_validate_when_application_created_no_details_captured(self, application_mock):
        """Test WorkPermitValidator.validate when all required that not provided.
        """
        application_mock.return_value = self.create_data()
        app = application(ApplicationStatusEnum.NEW.value)

        validator = ResidentPermitValidator(
           process=app.process_name,
           work_resident_permit=None,
           document_number=app.application_document.document_number)
        self.assertFalse(validator.is_valid())
        self.assertGreater(len(validator.response.messages), 1)
        error_message = "Incorrect document number"
        statusError = error_message in [message.message for message in validator.response.messages]
        self.assertFalse(statusError)
        self.assertEqual(len(validator.response.messages), 9)

    @patch('app.models.Application.objects.get')
    def test_validate_when_personal_details_captured_true(self, application_mock):
        """Test WorkPermitValidator.validate when all required that are provided.
        """
        faker = Faker()
        application_mock.return_value = self.create_data()
        app = application(ApplicationStatusEnum.NEW.value)

        validator = ResidentPermitValidator(
           process=app.process_name,
           work_resident_permit=None,
           document_number=app.application_document.document_number)

        Person.objects.get_or_create(
            document_number=app.application_document.document_number,
            application_version=None,
            first_name=faker.unique.first_name(),
            last_name=faker.unique.last_name(),
            dob=faker.date_of_birth(minimum_age=18, maximum_age=65),
            middle_name=faker.first_name(),
            marital_status=faker.random_element(elements=('single', 'married', 'divorced')),
            country_birth=faker.country(),
            place_birth=faker.city(),
            gender=faker.random_element(elements=('male', 'female')),
            occupation=faker.job(),
            qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd'))
        )

        self.assertFalse(validator.is_valid())
        self.assertGreater(len(validator.response.messages), 1)
        self.assertEqual(len(validator.response.messages), 8)

    @patch('app.models.Application.objects.get')
    def test_validate_when_all_required_captured(self, application_mock):
        """Test WorkPermitValidator.validate when all required that not provided.
        """
        faker = Faker()
        application_mock.return_value = self.create_data()
        app = application(ApplicationStatusEnum.NEW.value)

        validator = ResidentPermitValidator(
           process=app.process_name,
           work_resident_permit=None,
           document_number=app.application_document.document_number)

        Person.objects.get_or_create(
            document_number=app.application_document.document_number,
            application_version=None,
            first_name=faker.unique.first_name(),
            last_name=faker.unique.last_name(),
            dob=faker.date_of_birth(minimum_age=18, maximum_age=65),
            middle_name=faker.first_name(),
            marital_status=faker.random_element(elements=('single', 'married', 'divorced')),
            country_birth=faker.country(),
            place_birth=faker.city(),
            gender=faker.random_element(elements=('male', 'female')),
            occupation=faker.job(),
            qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd'))
        )

        country = Country.objects.create(name=faker.country())
        # temp = Country.objects.filter(name=faker)
        ApplicationAddress.objects.create(
            application_version=None,
            document_number=app.application_document.document_number,
            po_box=faker.address(),
            apartment_number=faker.building_number(),
            plot_number=faker.building_number(),
            address_type=faker.random_element(elements=('residential', 'postal', 'business', 'private',
                                                        'other')),
            country=country,
            status=faker.random_element(elements=('active', 'inactive')),
            city=faker.city(),
            street_address=faker.street_name(),
            private_bag=faker.building_number(),
        )

        ApplicationContact.objects.create(
            application_version=None,
            document_number=app.application_document.document_number,
            contact_type=faker.random_element(elements=('cell', 'email', 'fax', 'landline')),
            contact_value=faker.phone_number(),
            preferred_method_comm=faker.boolean(chance_of_getting_true=50),
            status=faker.random_element(elements=('active', 'inactive')),
            description=faker.text(),
        )

        Passport.objects.create(
            application_version=None,
            document_number=app.application_document.document_number,
            passport_number=faker.passport_number(),
            date_issued=faker.date_this_century(),
            expiry_date=faker.date_this_century(),
            place_issued=faker.city(),
            nationality=faker.country(),
            photo=faker.image_url(),
        )

        classifer_attachment_types = ClassifierItem.objects.filter(
            code__in=['PASSPORT_COPY', 'PASSPORT_PHOTO', 'COVER_LETTER']
        )

        for classifier in classifer_attachment_types:
            attachment_type = AttachmentDocumentType.objects.create(
                code=classifier.code,
                name=classifier.name,
                valid_from=date.today(),
                valid_to=date(2025, 1, 1)
            )
            ApplicationAttachment.objects.create(
                document_number=app.application_document.document_number,
                document_type=attachment_type,
                filename="test.pdf",
                storage_object_key ="cxxcc",
                description="NNNN",
                document_url="",
                received_date=date.today()
            )
        ResidencePermit.objects.get_or_create(
            application_version=None,
            document_number=app.application_document.document_number,
            language=faker.language_code(),
            permit_reason=faker.text(),
            previous_nationality=faker.country(),
            current_nationality=faker.country(),
            state_period_required=faker.date_this_century(),
            propose_work_employment=faker.random_element(elements=('yes', 'no')),
            reason_applying_permit=faker.random_element(elements=('dependent', 'volunteer', 'student',
                                                                  'immigrant', 'missionary')),
            documentary_proof=faker.text(),
            travelled_on_pass=faker.text(),
            is_spouse_applying_residence=faker.random_element(elements=('yes', 'no')),
            ever_prohibited=faker.text(),
            sentenced_before=faker.text(),
            entry_place=faker.city(),
            arrival_date=faker.date_this_century(),
        )

        self.assertTrue(validator.is_valid())
        self.assertEqual(len(validator.response.messages), 0)

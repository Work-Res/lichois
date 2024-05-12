import os

from django.test import TestCase
from datetime import date

from unittest.mock import patch

from ..validators import WorkResidentPermitValidator

from app.models import Application, ApplicationDocument, ApplicationStatus, ApplicationUser
from app_personal_details.models import Person
from app_checklist.classes import CreateChecklist
from app.utils import ApplicationStatuses

from faker import Faker


def application(status):
    try:
        obj = Application.objects.get(application_status__status=status)
        return obj
    except Application.DoesNotExist:
        return None


class TestWorkResidentPermitValidator(TestCase):

    def create_data(self):
        file_name = "attachment_documents.json"
        output_file = os.path.join(os.getcwd(), "app_checklist", "data", file_name)
        create = CreateChecklist()
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
        """Test WorkResidentPermitValidator.validate when all required that not provided.
        """
        validator = WorkResidentPermitValidator(
           process=None,
           work_resident_permit=None,
           document_number=None)
        self.assertFalse(validator.is_valid())
        self.assertGreater(len(validator.response.messages), 1)
        self.assertEqual(len(validator.response.messages), 6)

    @patch('app.models.Application.objects.get')
    def test_validate_when_application_created_no_details_captured(self, application_mock):
        """Test WorkResidentPermitValidator.validate when all required that not provided.
        """
        application_mock.return_value = self.create_data()
        app = application(ApplicationStatuses.NEW.value)

        validator = WorkResidentPermitValidator(
           process=app.process_name,
           work_resident_permit=None,
           document_number=app.application_document.document_number)
        self.assertFalse(validator.is_valid())
        self.assertGreater(len(validator.response.messages), 1)
        error_message = "Incorrect document number"
        statusError = error_message in [message.message for message in validator.response.messages]
        self.assertFalse(statusError)
        self.assertEqual(len(validator.response.messages), 5)

    @patch('app.models.Application.objects.get')
    def test_validate_when_personal_details_captured(self, application_mock):
        """Test WorkResidentPermitValidator.validate when all required that not provided.
        """
        faker = Faker()
        application_mock.return_value = self.create_data()
        app = application(ApplicationStatuses.NEW.value)

        validator = WorkResidentPermitValidator(
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
        self.assertEqual(len(validator.response.messages), 4)

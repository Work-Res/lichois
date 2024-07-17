import os
import glob

from datetime import date

from faker import Faker

from app.models import ApplicationStatus
from app.classes import ApplicationService
from app_checklist.classes import CreateChecklistService

from app.api import NewApplicationDTO

from app_personal_details.models import Person, Passport
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact

from app_checklist.models import ClassifierItem
from app_attachments.models import ApplicationAttachment, AttachmentDocumentType
from app.utils import ApplicationStatusEnum

from app.utils import statuses
from django.test import TestCase

from citizenship.utils import CitizenshipProcessEnum


class BaseSetup(TestCase):

    def create_new_application(self):
        self.new_application_dto = NewApplicationDTO(
            process_name=CitizenshipProcessEnum.RENUNCIATION.value.lower(),
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.NEW.value,
            dob="06101990",
            work_place="01",
            full_name="Test test"
        )

        self.application_service = ApplicationService(
            new_application_dto=self.new_application_dto)
        return self.application_service.create_application()

    def create_checklist_records(self):
        file_name = "attachment_documents.json"
        output_file = os.path.join(os.getcwd(), "app_checklist", "data", "checklist", file_name)

        checklist_service = CreateChecklistService(
            parent_classifier_name="classifiers",
            child_name="classifier_items",
            foreign_name="checklist_classifier",
            parent_app_label_model_name="app_checklist.checklistclassifier",
            foreign_app_label_model_name="app_checklist.checklistclassifieritem")

        checklist_service.create(file_location=output_file)

        folder_path = os.path.join(os.getcwd(), "app_checklist", "data", "workflow")
        # Get a list of all JSON files in the folder
        file_list = glob.glob(os.path.join(folder_path, '*.json'))

        for file in file_list:
            if os.path.isfile(file):
                workflow_service = CreateChecklistService(
                    parent_classifier_name="classifiers",
                    child_name="classifier_items",
                    foreign_name="classifier",
                    parent_app_label_model_name="app_checklist.classifier",
                    foreign_app_label_model_name="app_checklist.classifieritem")
                workflow_service.create(file_location=file)

    def create_application_statuses(self):
        for status in statuses:
            ApplicationStatus.objects.create(
                **status
            )

    def create_personal_details(self, application, faker):
        return Person.objects.get_or_create(
            document_number=application.application_document.document_number,
            application_version=None,
            first_name=application.unique.first_name(),
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

    def create_address(self, app, faker):
        country = Country.objects.create(name=faker.country())
        return ApplicationAddress.objects.create(
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

    def setUp(self) -> None:

        self.create_checklist_records()
        self.create_application_statuses()
        application_version = self.create_new_application()

        app = application_version.application
        self.application = application_version.application
        self.document_number = app.application_document.document_number
        faker = Faker()
        self.create_personal_details(app, faker)
        self.create_address()

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
        # Checklist for process
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
                filename=f"{classifier.name}.pdf",
                storage_object_key="cxxcc",
                description="NNNN",
                document_url="",
                received_date=date.today()
            )

        self.application_decision_type()
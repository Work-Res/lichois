import os
import glob

from random import randint

from datetime import date
from django.test import TestCase

from faker import Faker

from app.models import Application, ApplicationStatus, ApplicationDecisionType
from app.classes import ApplicationService
from app_checklist.classes import CreateChecklistService

from app.api import NewApplicationDTO
from app.utils import ApplicationProcesses

from app_personal_details.models import Person, Passport
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact

from app_checklist.models import ClassifierItem
from app_attachments.models import ApplicationAttachment, AttachmentDocumentType
from app.utils import ApplicationStatusEnum

from workresidentpermit.models import WorkPermit, CommissionerDecision
from workresidentpermit.classes import WorkResidentPermitApplication


from workflow.models import Task
from model_mommy import mommy

from app.utils import statuses, ApplicationDecisionEnum
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


def application(status):
    try:
        obj = Application.objects.get(application_status__status=status)
        return obj
    except Application.DoesNotExist:
        return None


class TestSpecialPermitWorkflow(TestCase):

    def application_decision_type(self):
        for value in [ApplicationDecisionEnum.ACCEPTED.value,
                      ApplicationDecisionEnum.APPROVED.value,
                      ApplicationDecisionEnum.PENDING.value,
                      ApplicationDecisionEnum.REJECTED.value]:
            ApplicationDecisionType.objects.create(
                code=value,
                name=value,
                process_types=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
                valid_from=date(2024, 1, 1),
                valid_to=date(2025, 1, 1)
            )

    def setUp(self):
        faker = Faker()
        self.board = mommy.make_recipe(
            'board.board', )

        file_name = "attachment_documents.json"
        output_file = os.path.join(os.getcwd(), "app_checklist", "data", "checklist", file_name)

        checklist_service = CreateChecklistService(parent_classifier_name="classifiers", child_name="classifier_items",
                                                   foreign_name="checklist_classifier",
                                                   parent_app_label_model_name="app_checklist.checklistclassifier",
                                                   foreign_app_label_model_name="app_checklist.checklistclassifieritem")
        checklist_service.create(file_location=output_file)

        folder_path = os.path.join(os.getcwd(), "app_checklist", "data", "workflow")
        # Get a list of all JSON files in the folder
        file_list = glob.glob(os.path.join(folder_path, '*.json'))

        for file in file_list:
            if os.path.isfile(file):
                workflow_service = CreateChecklistService(parent_classifier_name="classifiers", child_name="classifier_items",
                                                          foreign_name="classifier",
                                                          parent_app_label_model_name="app_checklist.classifier",
                                                          foreign_app_label_model_name="app_checklist.classifieritem")
                workflow_service.create(file_location=file)

        for status in statuses:
            ApplicationStatus.objects.create(
                **status
            )
        process_name = ApplicationProcesses.SPECIAL_PERMIT.name
        application_type = WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_EMERGENCY.name

        fname = faker.unique.first_name()
        lname = faker.unique.last_name()

        new_app = NewApplicationDTO(
            application_type=application_type,
            process_name=process_name,
            applicant_identifier=f'{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}',
            status=ApplicationStatusEnum.NEW.value,
            dob='1990-06-10',
            work_place=randint(1000, 9999),
            full_name=f'{fname} {lname}'
        )

        self.application_service = ApplicationService(new_application=new_app)
        application_version = self.application_service.create_application()
        print(self.application_service.response.messages)
        print("application_version application_version ", application_version)

        app = application_version.application
        self.application = application_version.application
        self.document_number = app.application_document.document_number
        faker = Faker()

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
                filename=f"{classifier.name}.pdf",
                storage_object_key="cxxcc",
                description="NNNN",
                document_url="",
                received_date=date.today()
            )

        WorkPermit.objects.create(
            application_version=None,
            document_number=app.application_document.document_number,
            permit_status=faker.random_element(elements=('new', 'renewal')),
            job_offer=faker.text(),
            qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd')),
            years_of_study=faker.random_int(min=1, max=10),
            business_name=faker.company(),
            type_of_service=faker.text(),
            job_title=faker.job(),
            job_description=faker.text(),
            renumeration=faker.random_int(min=10000, max=100000),
            period_permit_sought=faker.random_int(min=1, max=10),
            has_vacancy_advertised=faker.boolean(chance_of_getting_true=50),
            have_funished=faker.boolean(chance_of_getting_true=50),
            reasons_funished=faker.text(),
            time_fully_trained=faker.random_int(min=1, max=10),
            reasons_renewal_takeover=faker.text(),
            reasons_recruitment=faker.text(),
            labour_enquires=faker.text(),
            no_bots_citizens=faker.random_int(min=1, max=10),
            name=faker.name(),
            educational_qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd')),
            job_experience=faker.text(),
            take_over_trainees=faker.first_name(),
            long_term_trainees=faker.first_name(),
            date_localization=faker.date_this_century(),
            employer=faker.company(),
            occupation=faker.job(),
            duration=faker.random_int(min=1, max=10),
            names_of_trainees=faker.first_name(),
        )

        self.application_decision_type()

    def test_workpermit_special_submission_when_verification_task_should_exists(self):
        """
        Check if all tasks created, the verification task should be created.
        """
        work_resident_permit_application = WorkResidentPermitApplication(
            document_number=self.document_number
        )

        response = work_resident_permit_application.submit()
        message = "Application has been submitted successfully."
        status = message in [message.get("details") for message in response.messages]
        self.assertTrue(status)

        tasks_count = Task.objects.filter(activity__process__document_number=self.document_number).count()
        self.assertEqual(tasks_count, 1)
        app = Application.objects.get(application_document__document_number=self.document_number)
        self.assertEqual(app.application_status.code.upper(), ApplicationStatusEnum.VERIFICATION.value.upper())

    def test_workpermit_special_when_done_with_verification_to_recommandation(self):
        """
        Check if all tasks created, the verification task should be created.
        """
        app_verification = ApplicationVerificationRequest()
        app_verification.comment = "Testing"
        app_verification.decision = "ACCEPTED"
        app_verification.outcome_reason = "UNKNOW"

        work_resident_permit_application = WorkResidentPermitApplication(
            document_number=self.document_number,
            verification_request=app_verification,
        )

        response = work_resident_permit_application.submit()
        message = "Application has been submitted successfully."
        status = message in [message.get("details") for message in response.messages]
        self.assertTrue(status)

        tasks_count = Task.objects.filter(activity__process__document_number=self.document_number).count()
        self.assertEqual(tasks_count, 1)
        app = Application.objects.get(application_document__document_number=self.document_number)
        self.assertEqual(app.application_status.code.upper(), ApplicationStatusEnum.VERIFICATION.value.upper())

        work_resident_permit_application.submit_verification()

        tasks_count = Task.objects.filter(activity__process__document_number=self.document_number).count()
        self.assertEqual(tasks_count, 2)
        app = Application.objects.get(application_document__document_number=self.document_number)
        self.assertEqual(app.application_status.code.upper(), ApplicationStatusEnum.RECOMMENDATION.value.upper())

    def test_workpermit_special_when_complete_recommandation_then_production(self):
        """
        Check if all tasks created, the commisioner's decision task should be created.
        """
        app_verification = ApplicationVerificationRequest()
        app_verification.comment = "Testing"
        app_verification.decision = "ACCEPTED"
        app_verification.outcome_reason = "UNKNOW"

        work_resident_permit_application = WorkResidentPermitApplication(
            document_number=self.document_number,
            verification_request=app_verification,
        )

        response = work_resident_permit_application.submit()
        message = "Application has been submitted successfully."
        status = message in [message.get("details") for message in response.messages]
        self.assertTrue(status)

        tasks_count = Task.objects.filter(activity__process__document_number=self.document_number).count()
        self.assertEqual(tasks_count, 1)
        app = Application.objects.get(application_document__document_number=self.document_number)
        self.assertEqual(app.application_status.code.upper(), ApplicationStatusEnum.VERIFICATION.value.upper())

        work_resident_permit_application.submit_verification()

        tasks_count = Task.objects.filter(activity__process__document_number=self.document_number).count()
        self.assertEqual(tasks_count, 2)
        app = Application.objects.get(application_document__document_number=self.document_number)
        self.assertEqual(app.application_status.code.upper(), ApplicationStatusEnum.RECOMMENDATION.value.upper())

        self.create_commissioner_decision()
        tasks_count = Task.objects.filter(activity__process__document_number=self.document_number).count()
        self.assertEqual(tasks_count, 3)
        app = Application.objects.get(application_document__document_number=self.document_number)
        self.assertEqual(app.application_status.code.upper(), ApplicationStatusEnum.ACCEPTED.value.upper())

    def create_commissioner_decision(self):
        CommissionerDecision.objects.create(
            document_number=self.document_number,
            date_requested=date.today(),
            date_approved=date.today(),
            status=ApplicationDecisionType.objects.get(code__iexact=ApplicationDecisionEnum.ACCEPTED.value),
            approved_by='test',
            summary="commissioner"
        )

from random import randint

from app_personal_details.models import Child, Spouse
from django.db.transaction import atomic
from faker import Faker

from app.utils.system_enums import ApplicationProcesses
from lichois.management.base_command import CustomBaseCommand
from workresidentpermit.model_mixins.employer_model_mixin import EmployerModelMixin
from workresidentpermit.models import ResidencePermit, WorkPermit
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


class Command(CustomBaseCommand):
    help = "Populate data for Work Application model"
    application_type = None
    process_name = ApplicationProcesses.WORK_PERMIT.value

    def handle(self, *args, **options):
        faker = Faker()
        work_res_permit = WorkResidentPermitApplicationTypeEnum.WORK_PERMIT_ONLY.value
        renewal_permit = WorkResidentPermitApplicationTypeEnum.WORK_PERMIT_RENEWAL.value
        replacement_permit = (
            WorkResidentPermitApplicationTypeEnum.WORK_PERMIT_REPLACEMENT.value
        )
        with atomic():

            for _ in range(50):
                self.application_type = faker.random_element(
                    elements=(work_res_permit, renewal_permit, replacement_permit)
                )
                app, version = self.create_basic_data()

                WorkPermit.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    permit_status=faker.random_element(elements=("new", "renewal")),
                    job_offer=faker.text(),
                    qualification=faker.random_element(
                        elements=("diploma", "degree", "masters", "phd")
                    ),
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
                    educational_qualification=faker.random_element(
                        elements=("diploma", "degree", "masters", "phd")
                    ),
                    job_experience=faker.text(),
                    take_over_trainees=faker.first_name(),
                    long_term_trainees=faker.first_name(),
                    date_localization=faker.date_this_century(),
                    employer=faker.company(),
                    occupation=faker.job(),
                    duration=faker.random_int(min=1, max=10),
                    names_of_trainees=faker.first_name(),
                )

                Child.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    age=randint(1, 18),
                    gender=faker.random_element(elements=("male", "female")),
                    is_applying_residence=faker.random_element(elements=("yes", "no")),
                )

                Spouse.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    middle_name=faker.first_name(),
                    maiden_name=faker.last_name(),
                    country=faker.country(),
                    dob=faker.date_of_birth(minimum_age=18, maximum_age=65),
                    place_birth=faker.city(),
                )

                self.stdout.write(self.style.SUCCESS("Successfully populated data"))

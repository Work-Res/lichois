from random import randint

from base_module.models import Child, Spouse
from django.db.transaction import atomic
from faker import Faker

from app.utils.system_enums import ApplicationProcesses
from lichois.management.base_command import CustomBaseCommand
from workresidentpermit.model_mixins.employer_model_mixin import EmployerModelMixin
from workresidentpermit.models import ResidencePermit, WorkPermit
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


class Command(CustomBaseCommand):
    help = "Populate data for Res Application model"
    application_type = None
    process_name = ApplicationProcesses.RESIDENT_PERMIT.value

    def handle(self, *args, **options):
        faker = Faker()
        work_res_permit = (
            WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_ONLY.value
        )
        renewal_permit = (
            WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_RENEWAL.value
        )
        replacement_permit = (
            WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_REPLACEMENT.value
        )
        with atomic():

            for _ in range(50):
                self.application_type = faker.random_element(
                    elements=(work_res_permit, renewal_permit, replacement_permit)
                )
                app, version = self.create_basic_data()
                ResidencePermit.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    language=faker.language_code(),
                    permit_reason=faker.text(),
                    previous_nationality=faker.country(),
                    current_nationality=faker.country(),
                    state_period_required=faker.date_this_century(),
                    propose_work_employment=faker.random_element(
                        elements=("yes", "no")
                    ),
                    reason_applying_permit=faker.random_element(
                        elements=(
                            "dependent",
                            "volunteer",
                            "student",
                            "immigrant",
                            "missionary",
                        )
                    ),
                    documentary_proof=faker.text(),
                    travelled_on_pass=faker.text(),
                    is_spouse_applying_residence=faker.random_element(
                        elements=("yes", "no")
                    ),
                    ever_prohibited=faker.text(),
                    sentenced_before=faker.text(),
                    entry_place=faker.city(),
                    arrival_date=faker.date_this_century(),
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

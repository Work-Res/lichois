from random import randint

from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.utils import ApplicationStatusEnum
from app_personal_details.models import Children, Spouse
from django.db.transaction import atomic
from faker import Faker

from app.utils.system_enums import ApplicationProcesses
from lichois.management.base_command import CustomBaseCommand
from workresidentpermit.models import ResidencePermit
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


class Command(CustomBaseCommand):
    help = "Populate data for Res Application model"
    application_type = ApplicationProcesses.RESIDENT_PERMIT_REPLACEMENT.value
    process_name = ApplicationProcesses.RESIDENT_PERMIT_REPLACEMENT.value

    def add_arguments(self, parser):
        # Adding an optional document_number argument
        parser.add_argument(
            "--document_number",
            type=str,
            help="Specify a document number for the application",
        )

    def create_new_application(self, fname, lname, document_number=None):
        # Use provided document_number or generate a new one if not provided
        applicant_identifier = (
            f"{randint(1000, 9999)}-{randint(1000, 9999)}-"
            f"{randint(1000, 9999)}-{randint(1000, 9999)}"
        )

        new_app = NewApplicationDTO(
            application_type=self.application_type,
            process_name=self.process_name,
            applicant_identifier=applicant_identifier,
            status=ApplicationStatusEnum.VERIFICATION.value,
            applicant_type=self.faker.random_element(elements=("employee", "investor")),
            dob="1990-06-10",
            work_place=randint(1000, 9999),
            full_name=f"{fname} {lname}",
            application_permit_type="replacement",
            document_number=document_number,
        )
        app_service = ApplicationService(new_application_dto=new_app)
        app, version = app_service.create_application()
        return app, version

    def handle(self, *args, **options):

        document_number = options.get("document_number")

        faker = Faker()
        with atomic():
            # Pass the document_number to create_new_application if provided
            fname = faker.first_name()
            lname = faker.last_name()
            app, version = self.create_new_application(fname, lname, document_number)

            ResidencePermit.objects.get_or_create(
                application_version=version,
                document_number=app.application_document.document_number,
                language=faker.language_code(),
                permit_reason=faker.text(),
                previous_nationality=faker.country(),
                current_nationality=faker.country(),
                state_period_required=faker.date_this_century(),
                propose_work_employment=faker.random_element(elements=("yes", "no")),
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

            Children.objects.get_or_create(
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

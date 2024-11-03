from random import randint

from faker import Faker
from django.db.transaction import atomic
from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.utils import ApplicationProcesses, ApplicationStatusEnum
from lichois.management.base_command import CustomBaseCommand
from permanent_residence.enums import PermanentResidenceApplicationTypeEnum
from permanent_residence.models.permanent_residence import PermanentResidence


class Command(CustomBaseCommand):
    help = "Populate data for Blue card service"
    process_name = ApplicationProcesses.PERMANENT_RESIDENCE_REPLACEMENT.value

    def add_arguments(self, parser):
        # Adding an optional document_number argument
        parser.add_argument(
            '--document_number',
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
            document_number=document_number
        )
        app_service = ApplicationService(new_application_dto=new_app)
        app, version = app_service.create_application()

        return app, version

    def handle(self, *args, **options):
        document_number = options.get('document_number')
        self.stdout.write(self.style.SUCCESS(f"Process name: {self.process_name}"))
        faker = Faker()

        self.application_type = faker.random_element(
            elements=(
                PermanentResidenceApplicationTypeEnum.PERMANENT_RESIDENCE_ONLY.value,
                PermanentResidenceApplicationTypeEnum.PERMANENT_RESIDENCE_10_YEARS.value,
            )
        )
        with atomic():
            # Pass the document_number to create_new_application if provided
            fname = faker.first_name()
            lname = faker.last_name()
            app, version = self.create_new_application(fname, lname, document_number)

            PermanentResidence.objects.get_or_create(
                application_version=version,
                document_number=app.application_document.document_number,
                investor_contribution=faker.text(),
                employee_contribution=faker.text(),
                any_other_resident=faker.name(),
                violated_terms_before=faker.text(),
                preferred_method_comm=faker.text(),
                language=faker.text(),
                spouse_applying_residence=faker.text(),
                prohibited_in_botswana=faker.text(),
                reasons_prohibited=faker.text(),
                imprisonment_any_country=faker.text(),
                reasons_imprisonment=faker.text(),
                permit_reasons=faker.text(),
                period_when_required=faker.date_this_century(),
                take_up_occupation=faker.text(),
                application_reason=faker.text(),
                application_reason_other=faker.text(),
                application_status=faker.text(),
            )

            self.stdout.write(
                self.style.SUCCESS("Successfully populated blue card data")
            )

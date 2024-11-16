from faker import Faker
from django.core.management import call_command


from app.classes.application_service import ApplicationService
from app.api.dto.new_application_dto import NewApplicationDTO
from app.models import Application
from app.utils.system_enums import ApplicationProcesses, ApplicationStatusEnum
from lichois.management.base_command import CustomBaseCommand
from ...classes.work_res_application_repository import ApplicationRepository
from ...models import ResidencePermit, WorkPermit
from app_personal_details.models.spouse import Spouse
from ...utils.work_resident_permit_application_type_enum import (
    WorkResidentPermitApplicationTypeEnum,
)
from app_checklist.models.system_parameter_permit_renewal_period import (
    SystemParameterPermitRenewalPeriod,
)


class Command(CustomBaseCommand):
    help = "Populates the database with renewal applications"

    def handle(self, *args, **options):

        call_command("populate_final_applications")

        for app in Application.objects.filter(
            process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
            application_status__code__iexact=ApplicationStatusEnum.ACCEPTED.value,
        ):
            document_number = app.application_document.document_number
            try:
                applicant = (
                    ApplicationRepository.get_application_user_by_document_number(
                        document_number
                    )
                )
            except Application.DoesNotExist:
                pass
            else:
                applicant_identifier = applicant.user_identifier
                self.create_replacement_applications(
                    document_number, applicant_identifier
                )
                self.create_renewal_permit(document_number, applicant_identifier)
        call_command("populate_work_res_attachment")

    def create_renewal_permit(self, document_number, applicant_identifier):
        SystemParameterPermitRenewalPeriod.objects.get_or_create(
            application_type=WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_RENEWAL.value,
            percent=0.25,
        )
        new_application_dto = NewApplicationDTO(
            process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT_RENEWAL.value,
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=ApplicationProcesses.WORK_RESIDENT_PERMIT_RENEWAL.value,
            full_name="Test test",
            applicant_type="student",
            application_permit_type="renewal",
            document_number=document_number,
            applicant_identifier=applicant_identifier,
        )
        application_service = ApplicationService(
            new_application_dto=new_application_dto
        )

        app, version = application_service.create_application()
        self.create_other_details(app, version)

    def create_replacement_applications(self, document_number, applicant_identifier):

        SystemParameterPermitRenewalPeriod.objects.get_or_create(
            application_type=WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_REPLACEMENT.value,
            percent=0.25,
        )
        new_application_dto = NewApplicationDTO(
            process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT_REPLACEMENT.value,
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=ApplicationProcesses.WORK_RESIDENT_PERMIT_REPLACEMENT.value,
            full_name="Test test",
            applicant_type="student",
            application_permit_type="replacement",
            document_number=document_number,
            applicant_identifier=applicant_identifier,
        )
        application_service = ApplicationService(
            new_application_dto=new_application_dto
        )

        app, version = application_service.create_application()

        self.create_other_details(app, version)
        # return app, version

    def create_other_details(self, app, version):
        faker = Faker()

        fname = faker.unique.first_name()
        lname = faker.unique.last_name()

        self.create_personal_details(app, version, lname, fname)

        self.create_application_address(app, version)

        self.create_application_contact(app, version)

        self.create_passport(app, version)

        self.create_education(app, version)

        self.create_parental_details(app, version)

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
            is_spouse_applying_residence=faker.random_element(elements=("yes", "no")),
            ever_prohibited=faker.text(),
            sentenced_before=faker.text(),
            entry_place=faker.city(),
            arrival_date=faker.date_this_century(),
        )

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

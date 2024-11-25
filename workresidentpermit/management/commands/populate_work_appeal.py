from django.core.management.base import BaseCommand
from app.api.dto.new_application_dto import NewApplicationDTO
from app.classes.application_service import ApplicationService
from app.utils.system_enums import ApplicationStatusEnum
from lichois.management.base_command import CustomBaseCommand
from faker import Faker

from app.utils import ApplicationProcesses
from ...classes.work_res_application_repository import ApplicationRepository
from workresidentpermit.models import PermitAppeal
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum
from app.models import Application
from django.core.management import call_command


class Command(CustomBaseCommand):
    help = "Populate data for Permit Appeals"
    application_type = None
    process_name = ApplicationProcesses.APPEAL_PERMIT.value
    faker = Faker()

    def handle(self, *args, **options):
        applications = Application.objects.filter(
            process_name=ApplicationProcesses.WORK_PERMIT.value,
            application_status__code__iexact=ApplicationStatusEnum.REJECTED.value,
        )
        if not applications.exists():
            self.stdout.write(self.style.WARNING("No applications found to process."))
            return
        for app in applications:
            document_number = app.application_document.document_number

            try:
                applicant = ApplicationRepository.get_application_user_by_document_number(
                    document_number
                )
                if not applicant or not hasattr(applicant, 'user_identifier'):
                    raise ValueError(f"Invalid applicant for document: {document_number}")
                
                applicant_identifier = applicant.user_identifier

                self.new_application_dto = NewApplicationDTO(
                    process_name=self.process_name,
                    status=ApplicationStatusEnum.VERIFICATION.value,
                    dob="06101990",
                    work_place="01",
                    application_type=WorkResidentPermitApplicationTypeEnum.WORK_PERMIT_APPEAL.value,
                    full_name="Test test",
                    applicant_type="student",
                    application_permit_type="appeal",
                    applicant_identifier=applicant_identifier,
                    document_number=document_number,
                )

                self.application_service = ApplicationService(
                    new_application_dto=self.new_application_dto
                )
                app, version = self.application_service.create_application()

                self.create_other_details(app, version)


            except Exception as e:
                self.stderr.write(f"Error processing document {document_number}: {e}")
            
        call_command("populate_appeal_attachments")


    def create_other_details(self, app, version):
        try:
            PermitAppeal.objects.get_or_create(
                application_version=version,
                document_number=app.application_document.document_number,
                appeal_type=self.faker.random_element(
                    elements=("appeal", "review", "renewal", "reconsideration")
                ),
                reason_for_appeal=self.faker.text(),
                appeal_date=self.faker.date_this_century(),
            )
        except Exception as e:
            self.stderr.write(f"Error creating appeal details for {app.application_document.document_number}: {e}")

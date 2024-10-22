from random import randint

from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from faker import Faker

from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.utils import ApplicationProcesses
from app.utils.system_enums import ApplicationStatusEnum
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact
from app_personal_details.models import Passport, Person
from workresidentpermit.models import PermitAppeal
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


class Command(BaseCommand):
    help = "Populate data for Populate data for Emergency & Exemption model"

    def handle(self, *args, **options):
        faker = Faker()
        process_name = ApplicationProcesses.APPEAL_PERMIT.name
        self.stdout.write(self.style.SUCCESS(f"Process name {process_name}"))
        # ApplicationStatus.objects.get_or_create(
        # 	code=ApplicationStatusEnum.NEW.value,
        # 	name=ApplicationStatusEnum.VERIFICATION.name,
        # 	processes=f'{process_name}, {ApplicationProcesses.WORK_RESIDENT_PERMIT.name}, '
        # 	          f'{ApplicationProcesses.WORK_PERMIT.name}, {ApplicationProcesses.RESIDENT_PERMIT.name}',
        # 	valid_from='2024-01-01',
        # 	valid_to='2026-12-31',
        # )
        # ApplicationStatus.objects.get_or_create(
        # 	code=ApplicationStatusEnum.VERIFICATION.value,
        # 	name=ApplicationStatusEnum.VERIFICATION.name,
        # 	processes=f'{process_name}, {ApplicationProcesses.WORK_RESIDENT_PERMIT.name}, '
        # 	          f'{ApplicationProcesses.WORK_PERMIT.name}, {ApplicationProcesses.RESIDENT_PERMIT.name}',
        # 	valid_from='2024-01-01',
        # 	valid_to='2026-12-31',
        # )

        for _ in range(150):
            with atomic():
                self.application_type = faker.random_element(
                    elements=(
                        WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_APPEAL.value,
                        WorkResidentPermitApplicationTypeEnum.WORK_PERMIT_APPEAL.value,
                        WorkResidentPermitApplicationTypeEnum.RESIDENT_PERMIT_APPEAL.value,
                        WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE_APPEAL.value,
                    )
                )
                self.stdout.write(self.style.SUCCESS("Populating appeal data..."))
                app, version = self.create_basic_data()

                PermitAppeal.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    appeal_type=faker.random_element(
                        elements=("appeal", "review", "renewal", "reconsideration")
                    ),
                    reason_for_appeal=faker.text(),
                    appeal_date=faker.date_this_century(),
                )

                self.stdout.write(self.style.SUCCESS("Successfully populated data"))

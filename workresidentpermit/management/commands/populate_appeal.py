from random import randint

from django.db.transaction import atomic
from lichois.management.base_command import CustomBaseCommand

from app.utils import ApplicationProcesses
from workresidentpermit.models import PermitAppeal
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


class Command(CustomBaseCommand):
    help = "Populate data for Populate data for Emergency & Exemption model"

    process_name = ApplicationProcesses.APPEAL_PERMIT.value
    application_type = elements=(
                        WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_APPEAL.value,
                        WorkResidentPermitApplicationTypeEnum.WORK_PERMIT_APPEAL.value,
                        WorkResidentPermitApplicationTypeEnum.RESIDENT_PERMIT_APPEAL.value,
                        WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE_APPEAL.value,
                    )
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

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
                app, version = self.create_basic_data()

                PermitAppeal.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    appeal_type=self.faker.random_element(
                        elements=("appeal", "review", "renewal", "reconsideration")
                    ),
                    reason_for_appeal=self.faker.text(),
                    appeal_date=self.faker.date_this_century(),
                )

                self.stdout.write(self.style.SUCCESS("Successfully populated data"))

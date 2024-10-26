from random import randint

from lichois.management.base_command import CustomBaseCommand
from django.db.transaction import atomic

from app.utils import ApplicationProcesses
from workresidentpermit.models import PermitCancellation
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


class Command(CustomBaseCommand):
    help = "Populate data for Populate data for Emergency & Exemption model"
    process_name = ApplicationProcesses.SPECIAL_PERMIT.value
    application_type = WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_CANCELLATION.value

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

    # def handle(self, *args, **options):
    #     faker = Faker()
    #     process_name = ApplicationProcesses.SPECIAL_PERMIT.name
    #     application_type = (
    #         WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_CANCELLATION.name
    #     )
        # ApplicationStatus.objects.get_or_create(
        # 	code='new',
        # 	name='New',
        # 	processes='EMERGENCY_PERMIT',
        # 	valid_from='2024-01-01',
        # 	valid_to='2026-12-31',
        # )
        for _ in range(150):

            with atomic():
                app, version = self.create_basic_data()

                PermitCancellation.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    cancellation_reasons=self.faker.sentence(),
                )

                self.stdout.write(self.style.SUCCESS("Successfully populated data"))

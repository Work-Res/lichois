from lichois.management.base_command import CustomBaseCommand
from django.db.transaction import atomic
from app.utils import ApplicationProcesses
from random import randint

from workresidentpermit.models import EmergencyPermit, ExemptionCertificate
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


class Command(CustomBaseCommand):
    help = "Populate data for Populate data for Emergency & Exemption model"
    process_name = ApplicationProcesses.SPECIAL_PERMIT.value
    application_type = WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_EMERGENCY.value

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

        # ApplicationStatus.objects.get_or_create(
        # 	code='new',
        # 	name='New',
        # 	processes='EMERGENCY_PERMIT',
        # 	valid_from='2024-01-01',
        # 	valid_to='2026-12-31',
        # )
        for _ in range(150):

            with atomic():
                permit_period = self.faker.random_element(
                        elements=("1 - 14 days", "15 - 90 days", "6 months")
                    )
                app, version = self.create_basic_data()
                
                app.permit_period = permit_period
                app.save()

                EmergencyPermit.objects.get_or_create(
                    document_number=app.application_document.document_number,
                    application_version=version,
                    nature_emergency=self.faker.random_element(
                        elements=("fire", "flood", "earthquake", "tsunami")
                    ),
                    emergency_period=permit_period,
                    job_requirements=self.faker.job(),
                    services_provided=self.faker.text(),
                    chief_authorization=self.faker.name(),
                    capacity=self.faker.random_element(
                        elements=("full-time", "part-time", "contract", "volunteer")
                    ),
                )

                self.stdout.write(self.style.SUCCESS("Successfully populated data"))

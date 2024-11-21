from django.core.management.base import BaseCommand
from app.utils.system_enums import ApplicationStatusEnum
from lichois.management.base_command import CustomBaseCommand
from faker import Faker

from app.utils import ApplicationProcesses
from workresidentpermit.models import PermitAppeal
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum
from app.models import Application


class Command(CustomBaseCommand):
    help = "Populate data for Permit Appeals"
    application_type = None
    process_name = ApplicationProcesses.APPEAL_PERMIT.value

    def handle(self, *args, **options):
        faker = Faker()
        applications = Application.objects.filter(
            process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
            application_status__code__iexact=ApplicationStatusEnum.ACCEPTED.value,
        )
        for app in applications:
            # self.application_type = faker.random_element(
            #     elements=(
            #         WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_APPEAL.value,
            #         WorkResidentPermitApplicationTypeEnum.WORK_PERMIT_APPEAL.value,
            #         WorkResidentPermitApplicationTypeEnum.RESIDENT_PERMIT_APPEAL.value,
            #         WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE_APPEAL.value,
            #     )
            # )

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

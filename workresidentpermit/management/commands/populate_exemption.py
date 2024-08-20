from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.utils import ApplicationProcesses
from app.utils.system_enums import ApplicationStatusEnum
from app_personal_details.models import Passport, Person
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact
from faker import Faker
from random import randint

from lichois.management.base_command import CustomBaseCommand
from workresidentpermit.models import ExemptionCertificate
from workresidentpermit.models.dependant import Dependant
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


class Command(CustomBaseCommand):
    help = "Populate data for Populate data for Exemption model"
    application_type = None
    process_name = ApplicationProcesses.EXEMPTION_CERTIFICATE.value

    def handle(self, *args, **options):
        faker = Faker()

        for _ in range(250):
            with atomic():
                self.application_type = faker.random_element(
                    elements=(
                        WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE.value,
                        WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE_RENEWAL.value,
                        WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE_REPLACEMENT.value,
                        WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE_CANCELLATION.value,
                    )
                )

                app, version = self.create_basic_data()
                ExemptionCertificate.objects.get_or_create(
                    document_number=app.application_document.document_number,
                    application_version=version,
                    business_name=faker.company(),
                    employment_capacity=faker.job(),
                    proposed_period=faker.random_element(
                        elements=("1 year", "2 years", "3 years", "4 years", "5 years")
                    ),
                )

                for _ in range(1, 5):
                    Dependant.objects.create(
                        application_version=version,
                        document_number=app.application_document.document_number,
                        name=faker.name(),
                        age=randint(1, 100),
                        gender=faker.random_element(
                            elements=("male", "female", "other")
                        ),
                    )

                self.stdout.write(self.style.SUCCESS("Successfully populated data"))

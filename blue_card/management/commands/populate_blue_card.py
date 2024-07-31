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
from app_personal_details.models.education import Education
from app_personal_details.models.next_of_kin import NextOfKin
from lichois.management.base_command import CustomBaseCommand
from ...enums import BlueCardApplicationTypeEnum


class Command(CustomBaseCommand):
    help = "Populate data for Populate data for Blue card service"
    process_name = ApplicationProcesses.BLUE_CARD_PERMIT.value
    application_type = BlueCardApplicationTypeEnum.BLUE_CARD_PERMIT_ONLY.value

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

        for _ in range(150):

            with atomic():
                app, version = self.create_basic_data()

                NextOfKin.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    first_name=self.faker.first_name(),
                    last_name=self.faker.last_name(),
                    relation=self.faker.random_element(
                        elements=("spouse", "parent", "child", "sibling")
                    ),
                    telephone=self.faker.phone_number(),
                    cell_phone=self.faker.phone_number(),
                )

                self.stdout.write(
                    self.style.SUCCESS("Successfully populated blue card data")
                )

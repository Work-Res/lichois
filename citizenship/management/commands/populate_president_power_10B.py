import factory
from faker import Faker

from django.db.transaction import atomic

from model_bakery import baker

from app_address.models import ApplicationAddress
from lichois.management.base_command import CustomBaseCommand
from ..factory.president_10b import (
    FormLFactory,
    NameChangeFactory,
    ResidencyPeriodFactory,
    LocalLanguageKnowledgeFactory,
)
from ...utils import CitizenshipProcessEnum, CitizenshipApplicationTypeEnum


class Command(CustomBaseCommand):
    help = "Populate data for registration of adopted child over 3 years old service"
    process_name = CitizenshipProcessEnum.PRESIDENT_POWER_10B.value
    application_type = CitizenshipApplicationTypeEnum.PRESIDENT_POWER_10B_ONLY.value

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

        fake = Faker()

        for _ in range(150):

            with atomic():
                app_service, application_version = self.create_basic_data()
                app = application_version.application
                fname = self.faker.unique.first_name()
                lname = self.faker.unique.last_name()

                father, created = self.create_personal_details(
                    application_version.application,
                    application_version,
                    fname,
                    lname,
                    person_type="father",
                )

                father_address = baker.make(
                    ApplicationAddress,
                    application_version=application_version,
                    document_number=app.application_document.document_number,
                    po_box=self.faker.address(),
                    person_type="father",
                    city=self.faker.city(),
                )

                mother, created = self.create_personal_details(
                    application_version.application,
                    application_version,
                    fname,
                    lname,
                    person_type="mother",
                )

                mother_address = baker.make(
                    ApplicationAddress,
                    application_version=application_version,
                    document_number=app.application_document.document_number,
                    po_box=self.faker.address(),
                    person_type="mother",
                    city=self.faker.city(),
                )

                sponsor, created = self.create_personal_details(
                    application_version.application,
                    application_version,
                    fname,
                    lname,
                    person_type="sponsor",
                )

                sponsor_address = baker.make(
                    ApplicationAddress,
                    application_version=application_version,
                    document_number=app.application_document.document_number,
                    po_box=self.faker.address(),
                    person_type="sponsor",
                    city=self.faker.city(),
                )

                witness, created = self.create_personal_details(
                    application_version.application,
                    application_version,
                    fname,
                    lname,
                    person_type="witness",
                )

                witness_address = baker.make(
                    ApplicationAddress,
                    application_version=application_version,
                    document_number=app.application_document.document_number,
                    po_box=self.faker.address(),
                    person_type="witness",
                    city=self.faker.city(),
                )

                form_l_instance = FormLFactory(
                    document_number=app.application_document.document_number,
                    father=father,
                    father_address=father_address,
                    mother=mother,
                    mother_address=mother_address,
                    sponsor=sponsor,
                    sponsor_address=sponsor_address,
                    witness=witness,
                    witness_address=witness_address,
                    name_change=NameChangeFactory(),
                    previous_application_date=fake.date(),
                    relation_description=fake.paragraph(),
                )

                form_l_instance.residency_periods.set(
                    [ResidencyPeriodFactory(), ResidencyPeriodFactory()]
                )
                form_l_instance.languages.set([LocalLanguageKnowledgeFactory()])

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully populated {self.process_name} data"
                    )
                )

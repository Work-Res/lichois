from django.db.transaction import atomic
from model_bakery import baker
from datetime import date

from app_address.models import ApplicationAddress
from app_contact.models import ApplicationContact
from app_personal_details.models import Person, Spouse
from lichois.management.base_command import CustomBaseCommand
from ...utils import CitizenshipProcessEnum, CitizenshipApplicationTypeEnum
from ...models import DCCertificate, OathOfAllegiance, ResidentialHistory
from ...models import DeclarationNaturalisationByForeignSpouse


class Command(CustomBaseCommand):
    help = "Populate data for registration of adopted child over 3 years old service"
    process_name = CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value
    application_type = CitizenshipApplicationTypeEnum.MATURITY_PERIOD_WAIVER_ONLY.value

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

        for _ in range(50):

            with atomic():
                fname = self.faker.unique.first_name()
                lname = self.faker.unique.last_name()

                # new_application
                app, version = self.create_new_application(fname, lname)

                # person
                # Applicant Personal Details
                baker.make(
                    Person,
                    first_name=fname,
                    last_name=lname,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    person_type="applicant",
                )

                # Applicant Residential Address Details
                baker.make(
                    ApplicationAddress,
                    application_version=version,
                    document_number=app.application_document.document_number,
                )

                # Spouse
                baker.make(
                    Spouse,
                    last_name=self.faker.unique.last_name(),
                    first_name=self.faker.unique.first_name(),
                    middle_name="",
                    maiden_name="",
                    dob=date(1990, 10, 6),
                    place_birth="BW"
                )

                # Applicant Postal Address Details
                baker.make(
                    ApplicationAddress,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    po_box=self.faker.address(),
                    address_type=self.faker.random_element(
                        elements=(
                            "residential",
                            "postal",
                            "business",
                            "private",
                            "other",
                        )
                    ),
                    private_bag=self.faker.building_number(),
                    city=self.faker.city(),
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        "Successfully populated Maturity Period Waiver data"
                    )
                )

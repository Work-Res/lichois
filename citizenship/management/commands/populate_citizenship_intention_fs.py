from datetime import date, timedelta
import random

from django.db.transaction import atomic
from model_bakery import baker
from faker import Faker


from lichois.management.base_command import CustomBaseCommand
from ...utils import CitizenshipProcessEnum, CitizenshipApplicationTypeEnum
from ...models import DeclarationNaturalisationByForeignSpouse, ResidentialHistory, OathOfAllegiance


class Command(CustomBaseCommand):
    help = "Populate data for declaration of intention by foreign spouse"
    process_name = CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value
    application_type = (
        CitizenshipApplicationTypeEnum.INTENTION_FOREIGN_SPOUSE_ONLY.value
    )

    def generate_random_date_range(self):
        """Generate random 'from' and 'to' dates within a reasonable range."""
        today = date.today()
        days_ago_start = random.randint(1, 365 * 5)  # Random date up to 5 years ago
        days_ago_end = random.randint(1, 365 * 2)  # Random date up to 2 years ago

        # Ensure the 'from' date is earlier than the 'to' date
        residence_from_date = today - timedelta(days=days_ago_start)
        residence_to_date = residence_from_date + timedelta(days=random.randint(30, 365))

        return residence_from_date, residence_to_date

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))
        fake = Faker()
        today = date.today()

        for _ in range(10):

            with atomic():
                fname = self.faker.unique.first_name()
                lname = self.faker.unique.last_name()

                # new_application
                app, version = self.create_basic_data()

                document_number = version.application.application_document.document_number

                from_date, to_date = self.generate_random_date_range()

                self.residence_history = baker.make(
                    ResidentialHistory,
                    country="Botswana",
                    residence_from_date=from_date,
                    residence_to_date=to_date
                )

                # Create a DeclarationNaturalisationByForeignSpouse instance using baker
                self.declaration = baker.make(
                    DeclarationNaturalisationByForeignSpouse,
                    application_residential_history=self.residential_history,
                    declaration_fname=fake.first_name(),
                    declaration_lname=fake.last_name(),
                    declaration_date=today,
                    signature=f"{fake.first_name()} {fake.last_name()}",
                    declaration_place=fake.city(),
                    oath_datetime=fake.date_time_this_decade(),
                    commissioner_name=f"{fake.first_name()} {fake.last_name()}",
                    commissioner_designation="Judge",
                    telephone_number=fake.phone_number(),
                    commissioner_signature="Signed by Commissioner",
                    application_version=version,
                    document_number=document_number
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        "Successfully populated citizenship intention by foreign spouse data"
                    )
                )

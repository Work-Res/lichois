from faker import Faker
from model_bakery import baker
from django.db.transaction import atomic

from datetime import date, timedelta

from lichois.management.base_command import CustomBaseCommand
from ...models import Naturalisation
from ...utils import CitizenshipProcessEnum

fake = Faker()


class Command(CustomBaseCommand):
    help = f"Populate data for {CitizenshipProcessEnum.NATURALIZATION.value} "
    process_name = CitizenshipProcessEnum.NATURALIZATION.value
    application_type = CitizenshipProcessEnum.NATURALIZATION.value

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

        for _ in range(50):

            with atomic():
                # new_application
                app_service, version = self.create_basic_data()
                document_number = version.application.application_document.document_number

                prev_application_date = date.today() - timedelta(days=fake.random_int(min=30, max=365 * 5))

                baker.make(
                    Naturalisation,
                    document_number=document_number,
                    birth_citizenship=fake.country(),
                    present_citizenship=fake.country(),
                    investment_level=f"${fake.random_int(min=10000, max=500000)}",
                    prev_application_date=prev_application_date,
                    name_change_particulars=fake.sentence(nb_words=10),
                    citizenship_change_particulars=fake.sentence(nb_words=15),
                    lost_citizenship_circumstances=fake.sentence(nb_words=20),
                    previous_convictions=fake.sentence(nb_words=12),
                    botswana_relations=fake.sentence(nb_words=8),
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully populated {CitizenshipProcessEnum.NATURALIZATION.value}"
                    )
                )

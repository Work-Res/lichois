from django.db.transaction import atomic
from model_bakery import baker

from faker import Faker
from datetime import date, timedelta, datetime

from app_checklist.models import ChecklistClassifier
from lichois.management.base_command import CustomBaseCommand
from ...models import KgosiCertificate, KgosanaCertificate, FormA, DCCertificate
from ...utils import CitizenshipProcessEnum


fake = Faker()


class Command(CustomBaseCommand):
    help = "Populate data for registration of adopted child over 3 years old service"
    process_name = CitizenshipProcessEnum.SETTLEMENT.value
    application_type = CitizenshipProcessEnum.SETTLEMENT.value

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

        for _ in range(50):

            with atomic():
                app_service, version = self.create_basic_data()
                known_year = date.today() - timedelta(days=fake.random_int(min=365 * 10, max=365 * 80))
                document_number = version.application.application_document.document_number

                settlement_year = date.today() - timedelta(days=fake.random_int(min=365 * 10, max=365 * 50))
                certificate_datetime = datetime.now() - timedelta(days=fake.random_int(min=1, max=365))

                kgosi_certificate = baker.make(
                    KgosiCertificate,
                    document_number=document_number,
                    kgosi_surname=fake.last_name(),
                    kgosi_firstname=fake.first_name(),
                    village=fake.city(),
                    tribe=fake.word(),
                    known_year=known_year,
                    community=fake.word(),
                    living_circumstance=fake.sentence(nb_words=15)
                )

                kgosana_certificate = baker.make(
                    KgosanaCertificate,
                    document_number=document_number,
                    kgosana_surname=fake.last_name(),
                    kgosana_firstname=fake.first_name(),
                    id_elder_firstname=fake.first_name(),
                    id_elder_lastname=fake.last_name(),
                    community=fake.city(),
                    settlement_year=settlement_year,
                    certificate_place=fake.address(),
                    certificate_datetime=certificate_datetime,
                    kgosana_sign=fake.name()
                )

                settlement_year = date.today() - timedelta(days=fake.random_int(min=365 * 10, max=365 * 50))
                declaration_datetime = datetime.now() - timedelta(days=fake.random_int(min=1, max=365))

                dc_certificate = baker.make(
                    DCCertificate,
                    dc_surname=fake.last_name(),
                    dc_firstname=fake.first_name(),
                    settlement_year=settlement_year,
                    origin_country=fake.country(),
                    community=fake.city(),
                    declaration_place=fake.address(),
                    declaration_datetime=declaration_datetime,
                    dc_sign=fake.name()
                )

                # Generate a random communication method from COMMUNICATION_CHOICES
                preferred_comm_method = fake.random_element(elements=[
                    'E-mail', 'SMS', 'POST', 'Telephone', 'Cellphone'
                ])

                baker.make(
                    FormA,
                    kgosi_certificate=kgosi_certificate,
                    kgosana_certificate=kgosana_certificate,
                    dc_certificate=dc_certificate,
                    preferred_method_of_comm=preferred_comm_method,
                    tribe_ordinarily_community_kgosi=fake.word(),
                    tribe_customarily_community_kgosi=fake.word(),
                    tribe_ordinarily_community_kgosana=fake.word(),
                    tribe_customarily_community_kgosana=fake.word()
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully populated Settlement data - {document_number}"
                    )
                )

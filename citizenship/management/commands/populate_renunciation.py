from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.models import ApplicationStatus
from app.utils.system_enums import ApplicationStatusEnum
from app_oath.models import OathDocument
from app_personal_details.models import Passport, Person
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact

from app.utils import statuses, ApplicationProcesses

from faker import Faker
from random import randint

from datetime import datetime

from authentication.models import User
from lichois.management.base_command import CustomBaseCommand
from .declarant_factory import DeclarantFactory

from .kgosana_certificate_factory import KgosanaCertificateFactory
from .kgosi_certificate_factory import KgosiCertificateFactory

from citizenship.models.renunciation import CertificateOfOrigin
from citizenship.utils import CitizenshipProcessEnum


class Command(CustomBaseCommand):

    help = "Populate data for Populate data for Citizenship Renunciation."
    process_name = CitizenshipProcessEnum.RENUNCIATION.value
    application_type = CitizenshipProcessEnum.RENUNCIATION.value

    def personal_details(self, person_type, version, fname, lname, app, faker):
        return Person.objects.get_or_create(
            application_version=version,
            first_name=fname,
            last_name=lname,
            document_number=app.application_document.document_number,
            dob=faker.date_of_birth(minimum_age=18, maximum_age=65),
            middle_name=faker.first_name(),
            marital_status=faker.random_element(
                elements=("single", "married", "divorced")
            ),
            country_birth=faker.country(),
            place_birth=faker.city(),
            gender=faker.random_element(elements=("male", "female")),
            occupation=faker.job(),
            qualification=faker.random_element(
                elements=("diploma", "degree", "masters", "phd")
            ),
            person_type=person_type,
        )

    def create_application_statuses(self):
        for status in statuses:
            ApplicationStatus.objects.get_or_create(
                code__iexact=status.get("code"), defaults=status
            )

    def create_certificate_of_origin(self, version, app, faker):

        father, created = self.personal_details(
            person_type="father",
            version=version,
            app=app,
            fname=faker.unique.first_name(),
            lname=faker.unique.last_name(),
            faker=faker,
        )
        mother, created = self.personal_details(
            person_type="mother",
            app=app,
            version=version,
            fname=faker.unique.first_name(),
            lname=faker.unique.last_name(),
            faker=faker,
        )

        declarant = DeclarantFactory()
        declarant.document_number = app.application_document.document_number
        declarant.save()

        verifier = User.objects.filter(username="tverification1").first()

        OathDocument.objects.create(
            document_number=app.application_document.document_number,
            user=verifier,
            content="Testing",
            created_at=datetime.today(),
            signed=True,
            signed_at=datetime.today(),
        )

        kgosi = KgosiCertificateFactory()
        kgosana = KgosanaCertificateFactory()

        certificate_of_origin = CertificateOfOrigin.objects.create(
            father=father, mother=mother, kgosi=kgosi, kgosana=kgosana
        )
        return certificate_of_origin

    def handle(self, *args, **options):
        faker = Faker()
        process_name = CitizenshipProcessEnum.RENUNCIATION.value
        self.stdout.write(self.style.SUCCESS(f"Process name {process_name}"))

        for _ in range(50):

            with atomic():
                app, version = self.create_basic_data()

                self.stdout.write(
                    self.style.SUCCESS("Successfully populated blue card data")
                )

                self.create_certificate_of_origin(version=version, app=app, faker=faker)

                self.stdout.write(self.style.SUCCESS("Successfully populated data"))

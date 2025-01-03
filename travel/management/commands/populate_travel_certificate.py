from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.utils import ApplicationProcesses
from app.utils.system_enums import ApplicationStatusEnum
from app_personal_details.models import Person
from app_address.models import ApplicationAddress, Country
from faker import Faker
from random import randint

from travel.models import ApplicantRelative, TravelCertificate
from ...utils import TravelCertificateEnum


class Command(BaseCommand):
    help = "Populate data for Populate data for Travel certificate"

    def handle(self, *args, **options):
        faker = Faker()
        process_name = ApplicationProcesses.TRAVEL_CERTIFICATE.value
        self.stdout.write(self.style.SUCCESS(f"Process name {process_name}"))
        for _ in range(50):
            fname = faker.unique.first_name()
            lname = faker.unique.last_name()
            with atomic():
                new_app = NewApplicationDTO(
                    application_type=TravelCertificateEnum.TRAVEL_CERTIFICATE.value,
                    process_name=process_name,
                    applicant_identifier=(
                        f"{randint(1000, 9999)}-{randint(1000, 9999)}-"
                        f"{randint(1000, 9999)}-{randint(1000, 9999)}"
                    ),
                    status=ApplicationStatusEnum.VERIFICATION.value,
                    dob="1990-06-10",
                    work_place=randint(1000, 9999),
                    full_name=f"{fname} {lname}",
                    applicant_type=faker.random_element(
                        elements=("employee", "investor")
                    ),
                )
                self.stdout.write(self.style.SUCCESS("Populating appeal data..."))
                app = ApplicationService(new_application_dto=new_app)
                self.stdout.write(self.style.SUCCESS(new_app.__dict__))
                app, version = app.create_application()
                Person.objects.get_or_create(
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
                )
                country = (Country.objects.create(name=faker.country()),)

                ApplicationAddress.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    po_box=faker.address(),
                    apartment_number=faker.building_number(),
                    plot_number=faker.building_number(),
                    address_type=faker.random_element(
                        elements=(
                            "residential",
                            "postal",
                            "business",
                            "private",
                            "other",
                        )
                    ),
                    country__id=country[0].id,
                    status=faker.random_element(elements=("active", "inactive")),
                    city=faker.city(),
                    street_address=faker.street_name(),
                    private_bag=faker.building_number(),
                )

                TravelCertificate.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    kraal_head_name=faker.name(),
                    chief_name=faker.name(),
                    clan_name=faker.name(),
                    issuing_authority=faker.name(),
                    names_of_other_relatives=faker.name(),
                    date_issued=faker.date_this_century(),
                    full_address_of_relative=faker.address(),
                    original_home_address=faker.address(),
                )
                address = ApplicationAddress.objects.create(
                    po_box=faker.address(),
                    apartment_number=faker.building_number(),
                    plot_number=faker.building_number(),
                    address_type=faker.random_element(
                        elements=(
                            "residential",
                            "postal",
                            "business",
                            "private",
                            "other",
                        )
                    ),
                    country=country[0],
                    status=faker.random_element(elements=("active", "inactive")),
                    city=faker.city(),
                    street_address=faker.street_name(),
                    private_bag=faker.building_number(),
                )

                ApplicantRelative.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    surname=faker.last_name(),
                    name=faker.first_name(),
                    relationship=faker.random_element(
                        elements=(
                            "father",
                            "mother",
                            "sister",
                            "brother",
                            "uncle",
                            "aunt",
                            "cousin",
                        )
                    ),
                    address=address,
                )

                self.stdout.write(self.style.SUCCESS("Successfully populated data"))

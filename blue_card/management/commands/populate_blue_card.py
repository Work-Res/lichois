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
from app_personal_details.models.next_of_kin import NextOfKin
from ...enums import BlueCardApplicationTypeEnum


class Command(BaseCommand):
    help = "Populate data for Populate data for Blue card service"

    def handle(self, *args, **options):
        faker = Faker()
        process_name = ApplicationProcesses.BLUE_CARD_PERMIT.value
        self.stdout.write(self.style.SUCCESS(f"Process name {process_name}"))

        for _ in range(150):
            fname = faker.unique.first_name()
            lname = faker.unique.last_name()
            with atomic():
                new_app = NewApplicationDTO(
                    application_type=BlueCardApplicationTypeEnum.BLUE_CARD_ONLY.value,
                    process_name=process_name,
                    applicant_identifier=(
                        f"{randint(1000, 9999)}-{randint(1000, 9999)}-"
                        f"{randint(1000, 9999)}-{randint(1000, 9999)}"
                    ),
                    status=ApplicationStatusEnum.VERIFICATION.value,
                    applicant_type=faker.random_element(
                        elements=("employee", "investor")
                    ),
                    dob="1990-06-10",
                    work_place=randint(1000, 9999),
                    full_name=f"{fname} {lname}",
                )
                app = ApplicationService(new_application=new_app)
                version = app.create_application()
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

                ApplicationContact.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    contact_type=faker.random_element(
                        elements=("cell", "email", "fax", "landline")
                    ),
                    contact_value=faker.phone_number(),
                    preferred_method_comm=faker.boolean(chance_of_getting_true=50),
                    status=faker.random_element(elements=("active", "inactive")),
                    description=faker.text(),
                )

                Passport.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    passport_number=faker.passport_number(),
                    date_issued=faker.date_this_century(),
                    expiry_date=faker.date_this_century(),
                    place_issued=faker.city(),
                    nationality=faker.country(),
                    photo=faker.image_url(),
                )

                NextOfKin.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    relation=faker.random_element(
                        elements=("spouse", "parent", "child", "sibling")
                    ),
                    telephone=faker.phone_number(),
                    cell_phone=faker.phone_number(),
                )

                self.stdout.write(
                    self.style.SUCCESS("Successfully populated blue card data")
                )
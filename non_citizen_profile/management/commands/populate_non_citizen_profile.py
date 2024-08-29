from django.core.management.base import BaseCommand
from faker import Faker
from identifier.non_citizen_identifier import NonCitizenIdentifier
from django.db import transaction
from ...models import (
    Address,
    ContactDetails,
    Education,
    NextOfKin,
    Passport,
    PersonalDetails,
)


class Command(BaseCommand):
    help = "Populate data for Res Application model"

    @transaction.atomic
    def handle(self, *args, **options):
        faker = Faker()

        for _ in range(200):
            identifier = self.make_new_identifier(faker.date_of_birth())
            print(f"Identifier: {identifier}")
            PersonalDetails.objects.create(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                middle_name=faker.first_name(),
                maiden_name=faker.first_name(),
                dob=faker.date_of_birth(),
                occupation=faker.job(),
                non_citizen_identifier=identifier,
            )
            Address.objects.create(
                street_address=faker.street_address(),
                city=faker.city(),
                country=faker.country(),
                address_type=faker.random_element(
                    elements=("residential", "business", "postal", "private")
                ),
                non_citizen_identifier=identifier,
                status=faker.random_element(elements=("active", "inactive")),
                private_bag=faker.building_number(),
                po_box=faker.building_number(),
            )

            ContactDetails.objects.create(
                document_number=faker.building_number(),
                telphone=faker.phone_number(),
                cellphone=faker.phone_number(),
                alt_cellphone=faker.phone_number(),
                email=faker.email(),
                alt_email=faker.email(),
                emergency_contact_name=faker.name(),
                emergency_contact_number=faker.phone_number(),
                non_citizen_identifier=identifier,
            )

            Education.objects.create(
                institution=faker.random_element(
                    elements=(
                        "UB",
                        "Both",
                        "BAC",
                        "BAISAGO",
                        "Limkokwing",
                        "ABM",
                        "Boitekanelo",
                        "GUC",
                    )
                ),
                field_of_study=faker.random_element(
                    elements=(
                        "Computer Science",
                        "Mathematics",
                        "Economics",
                        "Physics",
                    )
                ),
                level=faker.random_element(
                    elements=(
                        "Bachelor's Degree",
                        "Master's Degree",
                        "Doctorate",
                        "Certificate",
                    )
                ),
                non_citizen_identifier=identifier,
                start_date=faker.date_this_century(),
                end_date=faker.date_this_century(),
            )

            NextOfKin.objects.create(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                relation=faker.random_element(
                    elements=("father", "mother", "sister", "brother", "uncle", "aunt")
                ),
                telephone=faker.phone_number(),
                cell_phone=faker.phone_number(),
                non_citizen_identifier=identifier,
            )

            Passport.objects.get_or_create(
                non_citizen_identifier=identifier,
                passport_number=faker.passport_number(),
                date_issued=faker.date_this_century(),
                expiry_date=faker.date_this_century(),
                place_issued=faker.city(),
                nationality=faker.country(),
                photo=faker.image_url(),
            )

    def make_new_identifier(self, dob):
        """Returns a new and unique identifier.

        Override this if needed.
        """
        non_citizen_identifier = NonCitizenIdentifier(
            dob=dob,
            label="non_citizen_identifier",
        )
        return non_citizen_identifier.identifier

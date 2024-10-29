from random import randint
from django.core.management.base import BaseCommand
from faker import Faker

from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.utils.system_enums import ApplicationStatusEnum
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact
from app_personal_details.models import Passport, Person
from ...app_personal_details.models.child import Child
from app_personal_details.models.education import Education


class CustomBaseCommand(BaseCommand):
    help = "Base command for all custom commands"
    process_name = None
    application_type = None
    faker = Faker()

    def __init__(self, *args, **kwargs):
        super(CustomBaseCommand, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        raise NotImplementedError("You must implement this method in your subclass")

    def create_basic_data(self):
        fname = self.faker.unique.first_name()
        lname = self.faker.unique.last_name()

        app, version = self.create_new_application(fname, lname)

        self.create_personal_details(app, version, lname, fname)

        self.create_application_address(app, version)

        self.create_application_contact(app, version)

        self.create_passport(app, version)

        self.create_education(app, version)

        self.create_parental_details(app, version)

        return app, version

    def create_new_application(self, fname, lname):
        new_app = NewApplicationDTO(
            application_type=self.application_type,
            process_name=self.process_name,
            applicant_identifier=(
                f"{randint(1000, 9999)}-{randint(1000, 9999)}-"
                f"{randint(1000, 9999)}-{randint(1000, 9999)}"
            ),
            status=ApplicationStatusEnum.VERIFICATION.value,
            applicant_type=self.faker.random_element(elements=("employee", "investor")),
            dob="1990-06-10",
            work_place=randint(1000, 9999),
            full_name=f"{fname} {lname}",
        )
        app_service = ApplicationService(new_application_dto=new_app)
        app, version = app_service.create_application()

        return app, version

    def create_personal_details(
        self, app, version, fname, lname, person_type="applicant"
    ):
        return Person.objects.get_or_create(
            application_version=version,
            first_name=fname,
            last_name=lname,
            document_number=app.application_document.document_number,
            dob=self.faker.date_of_birth(minimum_age=18, maximum_age=65),
            middle_name=self.faker.first_name(),
            marital_status=self.faker.random_element(
                elements=("single", "married", "divorced")
            ),
            country_birth=self.faker.country(),
            place_birth=self.faker.city(),
            gender=self.faker.random_element(elements=("male", "female")),
            occupation=self.faker.job(),
            qualification=self.faker.random_element(
                elements=("diploma", "degree", "masters", "phd")
            ),
            previous_nationality=self.faker.country(),
            previous_botswana_id_no=self.faker.random_number(digits=9, fix_len=True),
            person_type=person_type,
        )

    def create_application_address(self, app, version, person_type="applicant"):
        country = Country.objects.create(name=self.faker.country())

        ApplicationAddress.objects.get_or_create(
            application_version=version,
            document_number=app.application_document.document_number,
            po_box=self.faker.address(),
            apartment_number=self.faker.building_number(),
            plot_number=self.faker.building_number(),
            address_type=self.faker.random_element(
                elements=(
                    "residential",
                    "postal",
                    "business",
                    "private",
                    "other",
                )
            ),
            country__id=country.id,
            status=self.faker.random_element(elements=("active", "inactive")),
            city=self.faker.city(),
            street_address=self.faker.street_name(),
            private_bag=self.faker.building_number(),
            person_type=person_type,
        )

    def create_application_contact(self, app, version):
        contact_type = ["cell", "email", "fax", "landline"]
        contact_value = {
            "cell": self.faker.phone_number(),
            "email": self.faker.email(),
            "fax": self.faker.phone_number(),
            "landline": self.faker.phone_number(),
        }

        selected_contact_type = self.faker.random_element(elements=contact_type)

        ApplicationContact.objects.get_or_create(
            application_version=version,
            document_number=app.application_document.document_number,
            contact_type=selected_contact_type,
            contact_value=contact_value[selected_contact_type],
            preferred_method_comm=self.faker.boolean(chance_of_getting_true=50),
            email=self.faker.email(),
            cell=self.faker.phone_number(),
        )

    def create_passport(self, app, version):
        Passport.objects.get_or_create(
            application_version=version,
            document_number=app.application_document.document_number,
            passport_number=self.faker.passport_number(),
            date_issued=self.faker.date_this_century(),
            expiry_date=self.faker.date_this_century(),
            place_issued=self.faker.city(),
            nationality=self.faker.country(),
            photo=self.faker.image_url(),
            previous_passport_number=self.faker.passport_number(),
        )

    def create_education(self, app, version):
        Education.objects.get_or_create(
            application_version=version,
            document_number=app.application_document.document_number,
            institution=self.faker.company(),
            field_of_study=self.faker.random_element(
                elements=(
                    "Computer Science",
                    "Information Technology",
                    "Business Administration",
                    "Accounting",
                    "Finance",
                    "Economics",
                    "Marketing",
                    "Human Resource Management",
                    "Supply Chain Management",
                    "Logistics",
                    "Procurement",
                    "Engineering",
                    "Medicine",
                    "Nursing",
                    "Pharmacy",
                    "Law",
                    "Education",
                    "Agriculture",
                    "Hospitality",
                    "Tourism",
                    "Culinary Arts",
                    "Architecture",
                    "Urban Planning",
                    "Public Health",
                    "Psychology",
                    "Sociology",
                    "Political Science",
                    "International Relations",
                    "Development Studies",
                )
            ),
            level=self.faker.random_element(
                elements=(
                    "High School",
                    "Associate Degree",
                    "Bachelor's Degree",
                    "Master's Degree",
                    "Doctorate",
                    "Diploma",
                    "Certificate",
                    "Vocational",
                    "Professional Degree",
                    "Technical Degree",
                    "Postgraduate Certificate",
                    "Other",
                )
            ),
            start_date=self.faker.date_this_century(),
            end_date=self.faker.date_this_century(),
        )

    def create_parental_details(self, app, person):

        Spouse.objects.get_or_create(
            document_number=app.application_document.document_number,
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            middle_name=faker.first_name(),
            maiden_name=faker.last_name(),
            country=faker.country(),
            dob=faker.date_of_birth(minimum_age=18, maximum_age=65),
            place_birth=faker.city(),
        )

        # Create father's details
        father, created = Person.objects.get_or_create(
            first_name=self.faker.first_name_male(),
            last_name=self.faker.last_name(),
            dob=self.faker.date_of_birth(minimum_age=40),
            gender="male",
            person_type="father",
            document_number=app.application_document.document_number,
        )

        # Create mother's details
        mother, created = Person.objects.get_or_create(
            first_name=self.faker.first_name_female(),
            last_name=self.faker.last_name(),
            dob=self.faker.date_of_birth(minimum_age=40),
            document_number=app.application_document.document_number,
            person_type="mother",
            gender="female",
        )

        for _ in range(3):
            # Create child's details
            Child.objects.get_or_create(
                document_number=app.application_document.document_number,
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                age=randint(1, 18),
                gender=self.faker.random_element(elements=("male", "female")),
                is_applying_residence=self.faker.random_element(elements=("yes", "no")),
            )

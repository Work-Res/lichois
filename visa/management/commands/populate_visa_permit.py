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
from app_personal_details.models.education import Education
from visa.models.visa_application import VisaApplication
from visa.models.visa_reference import VisaReference

from ...enums import VisaApplicationTypeEnum


class Command(BaseCommand):
    help = "Populate data for Populate data for Blue card service"

    def handle(self, *args, **options):
        faker = Faker()
        process_name = ApplicationProcesses.VISA_PERMIT.value
        self.stdout.write(self.style.SUCCESS(f"Process name {process_name}"))

        for _ in range(150):
            fname = faker.unique.first_name()
            lname = faker.unique.last_name()
            with atomic():
                new_app = NewApplicationDTO(
                    application_type=VisaApplicationTypeEnum.VISA_PERMIT_ONLY.value,
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
                app = ApplicationService(new_application_dto=new_app)
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

                Education.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    institution=faker.company(),
                    field_of_study=faker.random_element(
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
                    level=faker.random_element(
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
                    start_date=faker.date_this_century(),
                    end_date=faker.date_this_century(),
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

                visa, _ = VisaApplication.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    visa_type=faker.random_element(
                        elements=(
                            "Tourist",
                            "Business",
                            "Transit",
                            "Student",
                            "Work",
                            "Medical",
                            "Conference",
                            "Official",
                            "Diplomatic",
                            "Other",
                        )
                    ),
                    no_of_entries=faker.random_element(elements=(1, 2, "multiple")),
                    durations_stay=faker.random_element(
                        elements=(
                            "1 month",
                            "3 months",
                            "6 months",
                            "1 year",
                            "2 years",
                            "3 years",
                            "4 years",
                            "5 years",
                            "10 years",
                        )
                    ),
                    travel_reasons=faker.text(),
                    requested_valid_from=faker.date_this_century(),
                    requested_valid_to=faker.date_this_century(),
                    return_visa_to=faker.address(),
                    return_valid_until=faker.date_this_century(),
                )

                for _ in range(2):
                    reference, _ = VisaReference.objects.get_or_create(
                        ref_first_name=faker.first_name(),
                        ref_last_name=faker.last_name(),
                        ref_tel_no=faker.phone_number(),
                        ref_res_permit_no=faker.random_int(min=100000, max=999999),
                        ref_id_no=faker.random_int(min=100000, max=999999),
                    )

                    visa.references.add(reference)
                    visa.save()

                self.stdout.write(
                    self.style.SUCCESS("Successfully populated blue card data")
                )

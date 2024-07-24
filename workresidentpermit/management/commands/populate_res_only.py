from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.utils import ApplicationProcesses
from app.utils.system_enums import ApplicationStatusEnum
from app_personal_details.models import Passport, Person
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact
from faker import Faker
from random import randint

from workresidentpermit.models import ResidencePermit, WorkPermit
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


class Command(BaseCommand):
    help = "Populate data for Work & Res Application model"

    def handle(self, *args, **options):
        faker = Faker()
        res_permit = WorkResidentPermitApplicationTypeEnum.RESIDENT_PERMIT_ONLY.name
        renewal_res = WorkResidentPermitApplicationTypeEnum.RESIDENT_PERMIT_RENEWAL.name
        replacement = (
            WorkResidentPermitApplicationTypeEnum.RESIDENT_PERMIT_REPLACEMENT.name
        )
        for _ in range(50):
            fname = faker.unique.first_name()
            lname = faker.unique.last_name()
            with atomic():
                new_app = NewApplicationDTO(
                    process_name=ApplicationProcesses.RESIDENT_PERMIT.name,
                    application_type=faker.random_element(
                        elements=(res_permit, renewal_res, replacement)
                    ),
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
                self.stdout.write(self.style.SUCCESS("Populating data..."))
                app = ApplicationService(new_application_dto=new_app)
                version = app.create_application()
                Person.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    first_name=fname,
                    last_name=lname,
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
                # temp = Country.objects.filter(name=faker)
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

                ResidencePermit.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    language=faker.language_code(),
                    permit_reason=faker.text(),
                    previous_nationality=faker.country(),
                    current_nationality=faker.country(),
                    state_period_required=faker.date_this_century(),
                    propose_work_employment=faker.random_element(
                        elements=("yes", "no")
                    ),
                    reason_applying_permit=faker.random_element(
                        elements=(
                            "dependent",
                            "volunteer",
                            "student",
                            "immigrant",
                            "missionary",
                        )
                    ),
                    documentary_proof=faker.text(),
                    travelled_on_pass=faker.text(),
                    is_spouse_applying_residence=faker.random_element(
                        elements=("yes", "no")
                    ),
                    ever_prohibited=faker.text(),
                    sentenced_before=faker.text(),
                    entry_place=faker.city(),
                    arrival_date=faker.date_this_century(),
                )

                self.stdout.write(self.style.SUCCESS("Successfully populated data"))

from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.utils import ApplicationProcesses
from app_personal_details.models import Passport, Person
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact
from faker import Faker
from random import randint

from workresidentpermit.models import ResidencePermit, WorkPermit


class Command(BaseCommand):
    help = 'Populate data for Work & Res Application model'

    def handle(self, *args, **options):
        faker = Faker()

        for _ in range(250):
            fname = faker.unique.first_name()
            lname = faker.unique.last_name()
            with atomic():
                new_app = NewApplicationDTO(
                    process_name=ApplicationProcesses.WORK_PERMIT.name,
                    application_type=faker.random_element(elements=('WORK_PERMIT', 'RENEWAL_PERMIT',
                                                                    'REPLACEMENT_PERMIT')),
                    applicant_identifier=f'{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}',
                    status='verification',
                    dob='1990-06-10',
                    work_place=randint(1000, 9999),
                    full_name=f'{fname} {lname}',
                )
                
                app = ApplicationService(new_application=new_app)
                version = app.create_application()
                Person.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    first_name=fname,
                    last_name=lname,
                    dob=faker.date_of_birth(minimum_age=18, maximum_age=65),
                    middle_name=faker.first_name(),
                    marital_status=faker.random_element(elements=('single', 'married', 'divorced')),
                    country_birth=faker.country(),
                    place_birth=faker.city(),
                    gender=faker.random_element(elements=('male', 'female')),
                    occupation=faker.job(),
                    qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd'))
                )
                country = Country.objects.create(name=faker.country()),
                # temp = Country.objects.filter(name=faker)
                ApplicationAddress.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    po_box=faker.address(),
                    apartment_number=faker.building_number(),
                    plot_number=faker.building_number(),
                    address_type=faker.random_element(elements=('residential', 'postal', 'business', 'private',
                                                                'other')),
                    country__id=country[0].id,
                    status=faker.random_element(elements=('active', 'inactive')),
                    city=faker.city(),
                    street_address=faker.street_name(),
                    private_bag=faker.building_number(),
                )

                ApplicationContact.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    contact_type=faker.random_element(elements=('cell', 'email', 'fax', 'landline')),
                    contact_value=faker.phone_number(),
                    preferred_method_comm=faker.boolean(chance_of_getting_true=50),
                    status=faker.random_element(elements=('active', 'inactive')),
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
    
                WorkPermit.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    permit_status=faker.random_element(elements=('new', 'renewal')),
                    job_offer=faker.text(),
                    qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd')),
                    years_of_study=faker.random_int(min=1, max=10),
                    business_name=faker.company(),
                    type_of_service=faker.text(),
                    job_title=faker.job(),
                    job_description=faker.text(),
                    renumeration=faker.random_int(min=10000, max=100000),
                    period_permit_sought=faker.random_int(min=1, max=10),
                    has_vacancy_advertised=faker.boolean(chance_of_getting_true=50),
                    have_funished=faker.boolean(chance_of_getting_true=50),
                    reasons_funished=faker.text(),
                    time_fully_trained=faker.random_int(min=1, max=10),
                    reasons_renewal_takeover=faker.text(),
                    reasons_recruitment=faker.text(),
                    labour_enquires=faker.text(),
                    no_bots_citizens=faker.random_int(min=1, max=10),
                    name=faker.name(),
                    educational_qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd')),
                    job_experience=faker.text(),
                    take_over_trainees=faker.first_name(),
                    long_term_trainees=faker.first_name(),
                    date_localization=faker.date_this_century(),
                    employer=faker.company(),
                    occupation=faker.job(),
                    duration=faker.random_int(min=1, max=10),
                    names_of_trainees=faker.first_name(),
                )
                self.stdout.write(self.style.SUCCESS('Successfully populated data'))

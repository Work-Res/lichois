from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.utils import ModuleProcessNameEnum
from app.utils.system_enums import ApplicationStatusEnum
from app_oath.models import OathDocument
from app_personal_details.models import Passport, Person
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact
from faker import Faker
from random import randint

from datetime import datetime

from authentication.models import User
from .declarant_factory import DeclarantFactory

from .kgosana_certificate_factory import KgosanaCertificateFactory
from .kgosi_certificate_factory import KgosiCertificateFactory

from citizenship.models.renunciation import FormR, CertificateOfOrigin
from citizenship.utils import CitizenshipApplicationTypeEnum
from .oath_document_factory import OathDocumentFactory


class Command(BaseCommand):
    help = 'Populate data  '

    def personal_details(self, person_type, version, fname, lname, app, faker):
        return Person.objects.get_or_create(
            application_version=version,
            first_name=fname,
            last_name=lname,
            document_number=app.application_document.document_number,
            dob=faker.date_of_birth(minimum_age=18, maximum_age=65),
            middle_name=faker.first_name(),
            marital_status=faker.random_element(elements=('single', 'married', 'divorced')),
            country_birth=faker.country(),
            place_birth=faker.city(),
            gender=faker.random_element(elements=('male', 'female')),
            occupation=faker.job(),
            qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd')),
            person_type=person_type
        )

    def create_form_r(self, version, app, faker):
        personal_details = self.personal_details(
            person_type='applicant',
            fname=faker.unique.first_name(),
            lname=faker.unique.last_name(),
            version=version,
            faker=faker,
            app=app
        )

        country = Country.objects.create(name=faker.country())

        address = ApplicationAddress.objects.get_or_create(
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

        declarant = DeclarantFactory()

        commissioner_of_oath = OathDocumentFactory()

        form_r = FormR.objects.create(
            personal_details=personal_details,
            address=address,
            declarant=declarant,
            commissioner_of_oath=commissioner_of_oath
        )
        return form_r

    def create_certificate_of_origin(self, version, app, faker):

        father = self.person(person_type='father',
                             app=app, fname=faker.unique.first_name(), lname=faker.unique.last_name(), faker=faker)
        mother = self.person(person_type='mother',
                             app=app, fname=faker.unique.first_name(), lname=faker.unique.last_name(),
                             faker=faker)

        declarant = DeclarantFactory()
        declarant.document_number = app.application_document.document_number
        declarant.save()

        verifier = User.objects.filter(username='tverification1').first()

        OathDocument.objects.create(
            document_number=app.application_document.document_number,
            user=verifier,
            content="Testing",
            created_at=datetime.today(),
            signed=True,
            signed_at=datetime.today()
        )

        kgosi = KgosiCertificateFactory()
        kgosana = KgosanaCertificateFactory()

        certificate_of_origin = CertificateOfOrigin.objects.create(
            father=father,
            mother=mother,
            kgosi=kgosi,
            kgosana=kgosana
        )
        return certificate_of_origin

    def handle(self, *args, **options):
        faker = Faker()
        process_name = ModuleProcessNameEnum.CITIZENSHIP.name
        self.stdout.write(self.style.SUCCESS(f'Process name {process_name}'))

        for _ in range(50):
            fname = faker.unique.first_name()
            lname = faker.unique.last_name()
            with atomic():
                new_app = NewApplicationDTO(
                    application_type=CitizenshipApplicationTypeEnum.RENUNCIATION.name,
                    process_name=process_name,
                    applicant_identifier=f'{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}',
                    status=ApplicationStatusEnum.VERIFICATION.value,
                    dob='1990-06-10',
                    work_place=randint(1000, 9999),
                    full_name=f'{fname} {lname}',
                )
                self.stdout.write(self.style.SUCCESS('Populating appeal data...'))
                app = ApplicationService(new_application=new_app)
                self.stdout.write(self.style.SUCCESS(new_app.__dict__))
                version = app.create_application()
                
                country = Country.objects.create(name=faker.country())
                
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

                Person.objects.get_or_create(
                    application_version=version,
                    first_name=fname,
                    last_name=lname,
                    document_number=app.application_document.document_number,
                    dob=faker.date_of_birth(minimum_age=18, maximum_age=65),
                    middle_name=faker.first_name(),
                    marital_status=faker.random_element(elements=('single', 'married', 'divorced')),
                    country_birth=faker.country(),
                    place_birth=faker.city(),
                    gender=faker.random_element(elements=('male', 'female')),
                    occupation=faker.job(),
                    qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd')),
                    person_type='applicant'
                )

                ApplicationContact.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    contact_type=faker.random_element(elements=('cell', 'email', 'fax', 'landline')),
                    contact_value=faker.phone_number(),
                    preferred_method_comm=faker.boolean(chance_of_getting_true=50),
                    status=faker.random_element(elements=('active', 'inactive')),
                    description=faker.text()
                )

                Passport.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    passport_number=faker.passport_number(),
                    date_issued=faker.date_this_century(),
                    expiry_date=faker.date_this_century(),
                    place_issued=faker.city(),
                    nationality=faker.country(),
                    photo=faker.image_url()
                )
                # add renunciation data
                form_r = self.create_form_r(version=version, app=app, faker=faker)
                certificate_of_origin = self.create_certificate_of_origin(version=version, app=app, faker=faker)

                self.stdout.write(self.style.SUCCESS('Successfully populated data'))

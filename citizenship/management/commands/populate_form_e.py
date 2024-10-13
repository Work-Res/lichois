from django.db.transaction import atomic
from citizenship.models.registration.form_e import FormE
from model_bakery import baker
from app_personal_details.models import Person
from lichois.management.base_command import CustomBaseCommand
from ...utils import CitizenshipProcessEnum, CitizenshipApplicationTypeEnum
from app_address.models import ApplicationAddress
from faker import Faker

class Command(CustomBaseCommand):
    help = "Populate data for Registration of Child under 21 years."

    process_name = CitizenshipProcessEnum.UNDER_20_CITIZENSHIP.value
    application_type = (
        CitizenshipApplicationTypeEnum.UNDER_20_CITIZENSHIP.value
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))
        fake = Faker()
        for _ in range(10):

            with atomic():
                fname = self.faker.unique.first_name()
                lname = self.faker.unique.last_name()

                app, version = self.create_new_application(fname, lname)

                guardian = baker.make(Person,
                                      application_version=version,
                                      document_number=app.application_document.document_number)
                father = baker.make(Person,
                                    application_version=version,
                                    document_number=app.application_document.document_number)
                mother = baker.make(Person,
                                    application_version=version,
                                    document_number=app.application_document.document_number)
                sponsor = baker.make(Person,application_version=version,
                                    document_number=app.application_document.document_number)
                witness = baker.make(Person,application_version=version,
                                    document_number=app.application_document.document_number)

                father_address = baker.make(ApplicationAddress)
                mother_address = baker.make(ApplicationAddress)
                sponsor_address = baker.make(ApplicationAddress)


                baker.make(FormE,
                    guardian=guardian,
                    citizenship_at_birth=fake.random_element(elements=['Yes', 'No']),
                    present_citizenship=fake.country(),
                    present_citizenship_not_available=fake.random_element(elements=['Yes', 'No']),
                    provide_circumstances=fake.text(max_nb_chars=300),
                    father=father,
                    father_address=father_address,
                    mother=mother,
                    mother_address=mother_address,
                    sponsor=sponsor,
                    sponsor_address=sponsor_address,
                    is_sponsor_signed=fake.boolean(),
                    sponsor_date_of_signature=fake.date(),
                    witness=witness,
                    witness_address=baker.make(ApplicationAddress)
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        "Successfully populated citizenship data for form E"
                    )
                )

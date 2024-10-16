from django.db.transaction import atomic
from model_bakery import baker

from app_address.models import ApplicationAddress
from app_checklist.models import Location
from lichois.management.base_command import CustomBaseCommand
from ...utils import CitizenshipProcessEnum, CitizenshipApplicationTypeEnum
from ...models import FormC


class Command(CustomBaseCommand):
    help = "Populate data for registration of adopted child over 3 years old service"
    process_name = CitizenshipProcessEnum.ADOPTED_CHILD_REGISTRATION.value
    application_type = CitizenshipApplicationTypeEnum.ADOPTED_CHILD_REGISTRATION_ONLY.value

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

        for _ in range(100):

            with atomic():
                # new_application
                app, version = self.create_basic_data()
                fname = self.faker.unique.first_name()
                lname = self.faker.unique.last_name()
                guardian = self.create_personal_details(version.application, version, fname, lname, person_type='guardian')
                guardian_address = baker.make(ApplicationAddress, application_version=version,
                                              document_number=app.application_document.document_number,
                                              po_box=self.faker.address(),
                                              person_type="guardian",
                                              city=self.faker.city())

                location = baker.make(Location)

                fname = self.faker.unique.first_name()
                lname = self.faker.unique.last_name()
                adoptive_parent = self.create_personal_details(
                    version.application, version, fname, lname,
                                                        person_type='adoptive_parent')

                adoptive_parent_address = baker.make(ApplicationAddress, application_version=version,
                                              document_number=app.application_document.document_number,
                                              po_box=self.faker.address(),
                                              person_type="adoptive_parent",
                                              city=self.faker.city())

                fname = self.faker.unique.first_name()
                lname = self.faker.unique.last_name()
                sponsor = self.create_personal_details(
                    version.application, version, fname, lname,
                    person_type='sponsor')

                sponsor_address = baker.make(ApplicationAddress, application_version=version,
                                document_number=app.application_document.document_number,
                                po_box=self.faker.address(),
                                person_type="sponsor",
                                city=self.faker.city())

                fname = self.faker.unique.first_name()
                lname = self.faker.unique.last_name()
                witness = self.create_personal_details(
                    version.application, version, fname, lname,
                    person_type='witness')

                witness_address = baker.make(ApplicationAddress, application_version=version,
                                document_number=app.application_document.document_number,
                                po_box=self.faker.address(),
                                person_type="witness",
                                city=self.faker.city())

                baker.make(FormC,
                           document_number=app.application_document.document_number,
                           guardian=guardian,
                           declaration_fname=self.faker.unique.first_name(),
                           declaration_lname=self.faker.unique.last_name(),
                           guardian_address=guardian_address,
                           location=location,
                           designation=self.faker.job(),
                           citizenship_at_birth=self.faker.country(),
                           present_citizenship=self.faker.country(),
                           present_citizenship_not_available=self.faker.random_element(elements=['Yes', 'No']),
                           provide_circumstances=self.faker.text(max_nb_chars=300),
                           adoptive_parent=adoptive_parent,
                           adoptive_parent_address=adoptive_parent_address,
                           sponsor=sponsor,
                           sponsor_address=sponsor_address,
                           is_sponsor_signed=self.faker.boolean(),
                           sponsor_date_of_signature=self.faker.date(),
                           witness=witness,
                           witness_address=witness_address)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated citizenship data for form-C"
            )
        )

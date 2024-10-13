from django.db.transaction import atomic
from app_address.models.application_address import ApplicationAddress
from app_checklist.models.location import Location
from app_personal_details.models.person import Person
from citizenship.models.registration.form_c import FormC
from model_bakery import baker

from lichois.management.base_command import CustomBaseCommand
from ...utils import CitizenshipProcessEnum, CitizenshipApplicationTypeEnum

class Command(CustomBaseCommand):
    help = "Populate data for Registration of Adopted Child Over 3 years old"

    process_name = CitizenshipProcessEnum.ADOPTED_CHILD_REGISTRATION.value
    application_type = (
        CitizenshipApplicationTypeEnum.ADOPTED_CHILD_REGISTRATION.value
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

        for _ in range(10):

            with atomic():
                fname = self.faker.unique.first_name()
                lname = self.faker.unique.last_name()

                app, version = self.create_new_application(fname, lname)

                guardian = baker.make(Person, application_version=version,
                                    document_number=app.application_document.document_number,
                                    person_type="guardian")
                guardian_address = baker.make(ApplicationAddress,application_version=version,
                                    document_number=app.application_document.document_number,
                                    po_box=self.faker.address(),
                                    person_type="guardian")
                location = baker.make(Location)
                adoptive_parent = baker.make(Person,application_version=version,
                    document_number=app.application_document.document_number,
                    person_type="adoptive_parent")
                sponsor = baker.make(Person,application_version=version,
                    document_number=app.application_document.document_number,
                    person_type="sponsor")
                witness = baker.make(Person,application_version=version,
                    document_number=app.application_document.document_number,
                    person_type="witness")

                baker.make(FormC,
                guardian=guardian,
                guardian_address=guardian_address,
                location=location,
                designation=self.faker.job(),
                citizenship_at_birth=self.faker.random_element(elements=['Yes', 'No']),
                present_citizenship=self.faker.country(),
                present_citizenship_not_available=self.faker.random_element(elements=['Yes', 'No']),
                provide_circumstances=self.faker.text(max_nb_chars=300),
                adoptive_parent=adoptive_parent,
                adoptive_parent_address=baker.make(ApplicationAddress),
                sponsor=sponsor,
                sponsor_address=baker.make(ApplicationAddress),
                is_sponsor_signed=self.faker.boolean(),
                sponsor_date_of_signature=self.faker.date(),
                witness=witness,
                witness_address=baker.make(ApplicationAddress))

                self.stdout.write(
                    self.style.SUCCESS(
                        "Successfully populated citizenship data for form-C"
                    )
                )

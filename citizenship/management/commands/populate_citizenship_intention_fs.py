from django.db.transaction import atomic
from app_address.models.application_address import ApplicationAddress
from app_contact.models.application_contact import ApplicationContact
from model_bakery import baker


from app_personal_details.models import Person
from lichois.management.base_command import CustomBaseCommand
from ...utils import CitizenshipProcessEnum, CitizenshipApplicationTypeEnum
from ...models import DeclarationNaturalisationByForeignSpouse, ResidentialHistory, OathOfAllegiance


class Command(CustomBaseCommand):
    help = "Populate data for registration of adopted child over 3 years old service"
    process_name = CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value
    application_type = (
        CitizenshipApplicationTypeEnum.INTENTION_FOREIGN_SPOUSE_ONLY.value
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

        for _ in range(10):

            with atomic():
                fname = self.faker.unique.first_name()
                lname = self.faker.unique.last_name()

                # new_application
                app, version = self.create_new_application(fname, lname)

                # self.create_basic_data()

                # Residential History
                residence_history = baker.make(
                    ResidentialHistory,
                    application_version=version,
                    document_number=app.application_document.document_number,
                )

                # TODO: PersonalDeclaration

                # Applicant Oath
                baker.make(
                    OathOfAllegiance,
                    application_version=version,
                    document_number=app.application_document.document_number,
                )

                # declarant_personal_info
                person = baker.make(
                    Person,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    person_type="declarant",
                )

                contact_type = ["cell", "email", "fax", "landline"]
                contact_value = {
                    "cell": self.faker.phone_number(),
                    "email": self.faker.email(),
                    "fax": self.faker.phone_number(),
                    "landline": self.faker.phone_number(),
                }

                selected_contact_type = self.faker.random_element(elements=contact_type)

                contact = baker.make(ApplicationContact,
                                    application_version=version,
                                    document_number=app.application_document.document_number,
                                    contact_type=selected_contact_type,
                                    contact_value=contact_value[selected_contact_type],
                                    preferred_method_comm=self.faker.boolean(chance_of_getting_true=50),
                                    status=self.faker.random_element(elements=("active", "inactive")),
                                    description=self.faker.text())

                address = baker.make(ApplicationAddress,
                                    application_version=version,
                                    document_number=app.application_document.document_number,
                                    po_box=self.faker.address())

                # Declarant Citizenship details
                baker.make(DeclarationNaturalisationByForeignSpouse,
                        application_version=version,
                        document_number=app.application_document.document_number,
                        birth_citizenship=self.faker.city,
                        present_citizenship=self.faker.country(),
                        other_prev_citizenship=self.faker.text(),
                        application_person=person,
                        application_contact=contact,
                        application_address=address,
                        application_residential_history=residence_history)


                self.stdout.write(
                    self.style.SUCCESS(
                        "Successfully populated citizenship intention by foreign spouse data"
                    )
                )

from django.db.transaction import atomic
from model_bakery import baker

from app_address.models import ApplicationAddress
from app_contact.models import ApplicationContact
from app_personal_details.models import Person
from lichois.management.base_command import CustomBaseCommand
from ...utils import CitizenshipProcessEnum, CitizenshipApplicationTypeEnum
from ...models import DCCertificate, OathOfAllegiance


class Command(CustomBaseCommand):
    help = "Populate data for registration of adopted child over 3 years old service"
    process_name = CitizenshipProcessEnum.ADOPTED_CHILD_REGISTRATION.value
    application_type = (
        CitizenshipApplicationTypeEnum.ADOPTED_CHILD_REGISTRATION_ONLY.value
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

        for _ in range(50):

            with atomic():
                fname = self.faker.unique.first_name()
                lname = self.faker.unique.last_name()

                # new_application
                app, version = self.create_new_application(fname, lname)

                # person
                # Applicant Personal Details
                baker.make(
                    Person,
                    first_name=fname,
                    last_name=lname,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    person_type="applicant",
                )

                # Applicant Residential Address Details
                baker.make(
                    ApplicationAddress,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    person_type="applicant",
                )

                # Applicant Postal Address Details
                baker.make(
                    ApplicationAddress,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    po_box=self.faker.address(),
                    address_type=self.faker.random_element(
                        elements=(
                            "residential",
                            "postal",
                            "business",
                            "private",
                            "other",
                        )
                    ),
                    private_bag=self.faker.building_number(),
                    city=self.faker.city(),
                )

                # Applicant Contact Details
                baker.make(
                    ApplicationContact,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    status=self.faker.random_element(elements=("active", "inactive")),
                )

                # Applicant Oath
                baker.make(OathOfAllegiance)

                # child_personal_info
                baker.make(
                    Person,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    person_type="child",
                )

                # Child Address Details
                baker.make(
                    ApplicationAddress,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    po_box=self.faker.address(),
                    address_type=self.faker.random_element(
                        elements=(
                            "residential",
                            "postal",
                            "business",
                            "private",
                            "other",
                        )
                    ),
                    private_bag=self.faker.building_number(),
                    city=self.faker.city(),
                )

                # Parent Personal Details
                baker.make(
                    Person,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    person_type="mother",
                )

                # Parent Address Details
                baker.make(
                    ApplicationAddress,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    po_box=self.faker.address(),
                    address_type=self.faker.random_element(
                        elements=(
                            "residential",
                            "postal",
                            "business",
                            "private",
                            "other",
                        )
                    ),
                    private_bag=self.faker.building_number(),
                    city=self.faker.city(),
                )

                # Sponsor’s Personal Details
                baker.make(
                    Person,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    person_type="sponsor",
                )

                # Sponsor’s Address Details
                baker.make(
                    ApplicationAddress,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    po_box=self.faker.address(),
                    address_type=self.faker.random_element(
                        elements=(
                            "residential",
                            "postal",
                            "business",
                            "private",
                            "other",
                        )
                    ),
                    private_bag=self.faker.building_number(),
                    city=self.faker.city(),
                )

                # Witness Personal Details
                baker.make(
                    Person,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    person_type="witness",
                )

                # Witness Address
                baker.make(
                    ApplicationAddress,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    po_box=self.faker.address(),
                    address_type=self.faker.random_element(
                        elements=(
                            "residential",
                            "postal",
                            "business",
                            "private",
                            "other",
                        )
                    ),
                    private_bag=self.faker.building_number(),
                    city=self.faker.city(),
                )

                # Additional Sponsor
                baker.make(
                    Person,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    person_type="sponsor",
                )

                # Additional Sponsor’s Address Details
                baker.make(
                    ApplicationAddress,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    po_box=self.faker.address(),
                    address_type=self.faker.random_element(
                        elements=(
                            "residential",
                            "postal",
                            "business",
                            "private",
                            "other",
                        )
                    ),
                    private_bag=self.faker.building_number(),
                    city=self.faker.city(),
                )

                # Additional Witness Personal Details
                baker.make(
                    Person,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    person_type="witness",
                )

                # Additional Witness Address
                baker.make(
                    ApplicationAddress,
                    application_version=version,
                    document_number=app.application_document.document_number,
                    po_box=self.faker.address(),
                    address_type=self.faker.random_element(
                        elements=(
                            "residential",
                            "postal",
                            "business",
                            "private",
                            "other",
                        )
                    ),
                    private_bag=self.faker.building_number(),
                    city=self.faker.city(),
                )

                # applicant declaration
                baker.make(DCCertificate)

                # Oath
                baker.make(OathOfAllegiance)

                # NOT_USED
                # country
                # app_address
                # app_contact
                # passport
                # education

                self.stdout.write(
                    self.style.SUCCESS(
                        "Successfully populated adopted child registration data"
                    )
                )

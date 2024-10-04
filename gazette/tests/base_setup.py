import random

from random import randint

from datetime import date

from faker import Faker

from app.models import ApplicationStatus
from app.classes import ApplicationService

from app.api import NewApplicationDTO
from app_checklist.api import LocationSerializer
from app_checklist.models.location import Location

from app_personal_details.models import Person, Passport
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact

from django.apps import apps
from app_checklist.apps import AppChecklistConfig

from app_checklist.models import ClassifierItem
from app_attachments.models import ApplicationAttachment, AttachmentDocumentType
from app.utils import ApplicationStatusEnum

from app.utils import statuses

from citizenship.utils import CitizenshipProcessEnum

from rest_framework.test import APITestCase


class BaseSetup(APITestCase):
    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app_config = apps.get_app_config('app_checklist')
        if isinstance(app_config, AppChecklistConfig):
            app_config.ready()

    def create_new_application(self, application_type=None):
        self.new_application_dto = NewApplicationDTO(
            process_name=CitizenshipProcessEnum.RENUNCIATION.value,
            applicant_identifier=(
                f"{randint(1000, 9999)}-{randint(1000, 9999)}-"
                f"{randint(1000, 9999)}-{randint(1000, 9999)}"
            ),
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=application_type or CitizenshipProcessEnum.RENUNCIATION.value,
            full_name=f"{self.faker.unique.first_name()} {self.faker.unique.last_name()}",
            applicant_type="student"
        )

        self.application_service = ApplicationService(
            new_application_dto=self.new_application_dto)
        return self.application_service.create_application()

    def create_application_statuses(self):
        for status in statuses:
            ApplicationStatus.objects.create(
                **status
            )

    def create_personal_details(self, application, faker):
        return Person.objects.get_or_create(
            document_number=application.application_document.document_number,
            application_version=None,
            first_name=faker.unique.first_name(),
            last_name=faker.unique.last_name(),
            dob=faker.date_of_birth(minimum_age=18, maximum_age=65),
            middle_name=faker.first_name(),
            marital_status=faker.random_element(elements=('single', 'married', 'divorced')),
            country_birth=faker.country(),
            place_birth=faker.city(),
            gender=faker.random_element(elements=('male', 'female')),
            occupation=faker.job(),
            qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd'))
        )

    def create_district(self):
        districts = ["Kweneng", "Ngwaketse", "Central", "North-East", "North-West", "Ghanzi", "Kgalagadi",
                     "Borolong"]
        for district in districts:
            Location.objects.create(
                code=district,
                name=district,
                location_type='DISTRICT',
                valid_from=date.today()
            )

    def _create_village(self, district_code, villages):
        district = Location.objects.get(
            code=district_code,
            location_type="DISTRICT"
        )
        for village_name in villages:
            Location.objects.create(
                parent_location=district,
                name=village_name,
                code=village_name,
                valid_from=date.today()
            )

    def create_village(self):

        kweneng_villages = ["Metsibotlhoko", "Maratshwane", "Botlhapatlou", "Medie", "Molepolole", "Gakutlo",
                            "Ditshukudu", "Mantshwabisi", "Monwane", "Thamaga", "Kubung", "Mmankgodi", "Mogonono",
                            "Hatsalatladi"]

        self._create_village(district_code="Kweneng", villages=kweneng_villages)

        ngwaketse_villages = ["Kanye", "Ranaka", "Lotlhakane West", "Gasita", "Lorolwana", "Pitseng", "Lekgolobotlo",
                              "Lotlhakane", "Molapowabojang", "Ralekgetho", "Moshaneng", "Ntlhantlhe"]

        self._create_village(district_code="Ngwaketse", villages=ngwaketse_villages)

        borolong_villages = ["Pitsane Siding", "Tlhareseleele", "Pitsana-Potokwe", "Rakhuna", "Malokaganyane", "Bethel",
                             "Dinatshana",
                             "Ngwatsau", "Ramatlabama", "Good Hope", "Hebron", "Makokwe"]

        self._create_village(district_code="Borolong", villages=borolong_villages)

        ghanzi_villages = ["Qabo", "Karakobis", "Groote Laagte", "Dekar", "Ghanzi", "New Xade",
                           "Charles Hill", "Kule", "Ncojane", "New Xanagas", "Kacgae", "Bere"]
        self._create_village(district_code="Ghanzi", villages=ghanzi_villages)

    def create_address(self, app, faker, village):
        country = Country.objects.create(name=faker.country())
        return ApplicationAddress.objects.create(
            application_version=None,
            document_number=app.application_document.document_number,
            po_box=faker.address(),
            apartment_number=faker.building_number(),
            plot_number=faker.building_number(),
            address_type=faker.random_element(elements=('residential', 'postal', 'business', 'private',
                                                        'other')),
            village=self.location_to_json(village),
            district=self.location_to_json(village.parent_location),
            country=country,
            status=faker.random_element(elements=('active', 'inactive')),
            city=faker.city(),
            street_address=faker.street_name(),
            private_bag=faker.building_number(),
        )

    def create_apps(self, villages):
        for village_name in villages:
            number = random.randint(1, 50)
            for _ in range(number):
                village = Location.objects.get(
                    name=village_name
                )
                app = self.create_new_application(application_type=CitizenshipProcessEnum.NATURALIZATION.value)
                self.create_address(app=app, faker=self.faker, village=village)

    def create_apps_villages(self):
        kweneng_villages = ["Metsibotlhoko", "Maratshwane", "Botlhapatlou", "Medie", "Molepolole", "Gakutlo",
                            "Ditshukudu", "Mantshwabisi", "Monwane", "Thamaga", "Kubung", "Mmankgodi", "Mogonono",
                            "Hatsalatladi"]
        self.create_apps(villages=kweneng_villages)

        ngwaketse_villages = ["Kanye", "Ranaka", "Lotlhakane West", "Gasita", "Lorolwana", "Pitseng", "Lekgolobotlo",
                              "Lotlhakane", "Molapowabojang", "Ralekgetho", "Moshaneng", "Ntlhantlhe"]
        self.create_apps(villages=ngwaketse_villages)

        borolong_villages = ["Pitsane Siding", "Tlhareseleele", "Pitsana-Potokwe", "Rakhuna", "Malokaganyane", "Bethel",
                             "Dinatshana",
                             "Ngwatsau", "Ramatlabama", "Good Hope", "Hebron", "Makokwe"]
        self.create_apps(villages=borolong_villages)

        ghanzi_villages = ["Qabo", "Karakobis", "Groote Laagte", "Dekar", "Ghanzi", "New Xade",
                           "Charles Hill", "Kule", "Ncojane", "New Xanagas", "Kacgae", "Bere"]
        self.create_apps(villages=ghanzi_villages)

    def location_to_json(self, location):
        if location:
            serializer = LocationSerializer(location)
            return serializer.data

    def setUp(self) -> None:

        self.create_district()
        self.create_village()
        self.create_application_statuses()
        application_version = self.create_new_application()

        app = application_version.application
        self.application = application_version.application
        self.document_number = app.application_document.document_number
        faker = Faker()
        self.create_personal_details(app, faker)
        self.create_address(app, faker)

        ApplicationContact.objects.create(
            application_version=None,
            document_number=app.application_document.document_number,
            contact_type=faker.random_element(elements=('cell', 'email', 'fax', 'landline')),
            contact_value=faker.phone_number(),
            preferred_method_comm=faker.boolean(chance_of_getting_true=50),
            status=faker.random_element(elements=('active', 'inactive')),
            description=faker.text(),
        )

        Passport.objects.create(
            application_version=None,
            document_number=app.application_document.document_number,
            passport_number=faker.passport_number(),
            date_issued=faker.date_this_century(),
            expiry_date=faker.date_this_century(),
            place_issued=faker.city(),
            nationality=faker.country(),
            photo=faker.image_url(),
        )
        # Checklist for process
        classifer_attachment_types = ClassifierItem.objects.filter(
            code__in=['PASSPORT_COPY', 'PASSPORT_PHOTO', 'COVER_LETTER']
        )

        for classifier in classifer_attachment_types:
            attachment_type = AttachmentDocumentType.objects.create(
                code=classifier.code,
                name=classifier.name,
                valid_from=date.today(),
                valid_to=date(2025, 1, 1)
            )
            ApplicationAttachment.objects.create(
                document_number=app.application_document.document_number,
                document_type=attachment_type,
                filename=f"{classifier.name}.pdf",
                storage_object_key="cxxcc",
                description="NNNN",
                document_url="",
                received_date=date.today()
            )

from django.urls import reverse
from datetime import datetime
from rest_framework import status

from app_oath.models import OathDocument
from app_personal_details.models import Person
from authentication.models import User
from .base_setup import BaseSetup

from faker import Faker

from rest_framework.test import APIClient

from ...management.commands.declarant_factory import DeclarantFactory
from ...management.commands.kgosana_certificate_factory import KgosanaCertificateFactory
from ...management.commands.kgosi_certificate_factory import KgosiCertificateFactory
from ...models.renunciation import CertificateOfOrigin


class TestRenunciationSummaryViewSetTests(BaseSetup):

    def setUp(self):
        faker = Faker()
        super().setUp()
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.create_certificate_of_origin(self.application_version, self.application_version.application, faker)

    def personal_details(self, person_type, version, fname, lname, app, faker):
        return Person.objects.get_or_create(
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
            person_type=person_type,
        )

    def create_certificate_of_origin(self, version, app, faker):

        father, created = self.personal_details(
            person_type="father",
            version=version,
            app=app,
            fname=faker.unique.first_name(),
            lname=faker.unique.last_name(),
            faker=faker,
        )
        mother, created = self.personal_details(
            person_type="mother",
            app=app,
            version=version,
            fname=faker.unique.first_name(),
            lname=faker.unique.last_name(),
            faker=faker,
        )

        declarant = DeclarantFactory()
        declarant.document_number = app.application_document.document_number
        declarant.save()

        verifier = User.objects.filter(username="tverification1").first()

        OathDocument.objects.create(
            document_number=app.application_document.document_number,
            user=verifier,
            content="Testing",
            created_at=datetime.today(),
            signed=True,
            signed_at=datetime.today(),
        )

        kgosi = KgosiCertificateFactory()
        kgosana = KgosanaCertificateFactory()

        certificate_of_origin = CertificateOfOrigin.objects.create(
            father=father, mother=mother, kgosi=kgosi, kgosana=kgosana,
            document_number=app.application_document.document_number
        )
        return certificate_of_origin


    def test_get_renunciation_summary_with_valid_document_number(self):
        """
        Ensure we can get the renunciation summary for a valid document number.
        """

        # Create the URL
        url = reverse('citizenship:renunciation-summary', kwargs={'document_number': self.document_number})
        # Make the GET request
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        application_address = response.data.get("application_address")
        self.assertIsNotNone(application_address)

        application_contact = response.data.get("application_contact")
        self.assertIsNotNone(application_contact)

        passport = response.data.get("passport")
        self.assertIsNotNone(passport)

        person = response.data.get("person")
        self.assertEqual(3, len(person))

    def test_get_renunciation_summary_with_invalid_document_number(self):
        """
        Ensure that an invalid document number returns appropriate response.
        """
        # Create the URL

        url = reverse('citizenship:renunciation-summary', kwargs={'document_number': "INVALIDDOC"})

        # Make the GET request
        response = self.client.get(url)

        # Assertions
        # Assuming the invalid document number causes a 404 or 400 depending on the logic in ApplicationSummary
        # Adjust the expected status code based on your actual implementation
        self.assertEqual(len(response.data), 0)

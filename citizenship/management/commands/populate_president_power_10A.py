from django.db.transaction import atomic
from model_bakery import baker

from app_address.models import ApplicationAddress
from app_checklist.models import ChecklistClassifier
from app_contact.models import ApplicationContact
from app_personal_details.models import Person
from lichois.management.base_command import CustomBaseCommand
from ...utils import CitizenshipProcessEnum


class Command(CustomBaseCommand):
    help = "Populate data for registration of adopted child over 3 years old service"
    process_name = CitizenshipProcessEnum.PRESIDENT_POWER_10A.value
    application_type = CitizenshipProcessEnum.PRESIDENT_POWER_10A.value

    def create_basic_data(self):
        fname = self.faker.unique.first_name()
        lname = self.faker.unique.last_name()

        app, version = self.create_new_application(fname, lname)

        self.create_personal_details(app, version, lname, fname)

        self.create_application_address(app, version)

        self.create_application_contact(app, version)

        return app, version

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

        for _ in range(5):

            with atomic():

                # new_application
                self.create_basic_data()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully populated {self.application_type}"
            )
        )

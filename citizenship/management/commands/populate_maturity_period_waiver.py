from django.db.transaction import atomic
from model_bakery import baker

from app.models import Application

from lichois.management.base_command import CustomBaseCommand
from ...models.maturity_period_waiver.maturity_period_waiver import MaturityPeriodWaiver
from ...utils import CitizenshipProcessEnum, CitizenshipApplicationTypeEnum


class Command(CustomBaseCommand):
    help = "Populate data for registration of adopted child over 3 years old service"
    process_name = CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value
    application_type = CitizenshipApplicationTypeEnum.MATURITY_PERIOD_WAIVER_ONLY.value

    def create_basic_data(self):
        fname = self.faker.unique.first_name()
        lname = self.faker.unique.last_name()

        app, version = self.create_new_application(fname, lname)

        self.create_personal_details(app, version, lname, fname)

        self.create_application_address(app, version)

        self.create_application_contact(app, version)

        return app, version

    def get_intention_document_number(self):
        excluded_document_numbers = MaturityPeriodWaiver.objects.values_list(
            "document_number_for_intention", flat=True
        )

        app = (
            Application.objects.filter(
                application_type=CitizenshipApplicationTypeEnum.INTENTION_FOREIGN_SPOUSE_ONLY.value,
                application_status__code="ACCEPTED",
            )
            .exclude(
                application_document__document_number__in=excluded_document_numbers
            )
            .first()
        )

        return app.application.application_document.document_number if app else ""

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

        for _ in range(50):
            with atomic():
                # new_application
                app_service, version = self.create_basic_data()
                document_number = (
                    version.application.application_document.document_number
                )

                baker.make(
                    MaturityPeriodWaiver,
                    document_number=document_number,
                    document_number_for_intention=self.get_intention_document_number(),
                    application_version=version,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully populated {self.application_type}"
                    )
                )

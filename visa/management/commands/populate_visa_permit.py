from random import randint

from lichois.management.base_command import CustomBaseCommand
from django.db.transaction import atomic

from app.utils import ApplicationProcesses
from visa.models.visa_application import VisaApplication
from visa.models.visa_reference import VisaReference

from ...enums import VisaApplicationTypeEnum


class Command(CustomBaseCommand):
    help = "Populate data for Visa"
    process_name = ApplicationProcesses.VISA_PERMIT.value
    application_type = VisaApplicationTypeEnum.VISA_PERMIT_ONLY.value

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

        for _ in range(150):

            with atomic():
                app, version = self.create_basic_data()

                visa, _ = VisaApplication.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    visa_type=self.faker.random_element(
                        elements=(
                            "Tourist",
                            "Business",
                            "Transit",
                            "Student",
                            "Work",
                            "Medical",
                            "Conference",
                            "Official",
                            "Diplomatic",
                            "Other",
                        )
                    ),
                    no_of_entries=self.faker.random_element(elements=("single", "multiple")),
                    proposed_durations_stay=self.faker.random_element(
                        elements=(
                            "1 month",
                            "3 months",
                            "6 months",
                            "1 year",
                            "2 years",
                            "3 years",
                            "4 years",
                            "5 years",
                            "10 years",
                        )
                    ),
                    travel_reasons=self.faker.text(),
                    requested_valid_from=self.faker.date_this_century(),
                    requested_valid_to=self.faker.date_this_century(),
                )

                for _ in range(2):
                    reference, _ = VisaReference.objects.get_or_create(
                        ref_first_name=self.faker.first_name(),
                        ref_last_name=self.faker.last_name(),
                        ref_tel_no=self.faker.phone_number(),
                        ref_res_permit_no=self.faker.random_int(min=100000, max=999999),
                        ref_id_no=self.faker.random_int(min=100000, max=999999),
                    )

                    visa.references.add(reference)
                    visa.save()

                self.stdout.write(
                    self.style.SUCCESS("Successfully populated Visa data")
                )

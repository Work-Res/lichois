from django.db.transaction import atomic
from faker import Faker

from app.utils import ApplicationProcesses
from lichois.management.base_command import CustomBaseCommand
from permanent_residence.enums import PermanentResidenceApplicationTypeEnum
from permanent_residence.models.permanent_residence import PermanentResidence


class Command(CustomBaseCommand):
    help = "Populate data for Populate data for Blue card service"
    process_name = ApplicationProcesses.PERMANENT_RESIDENCE.value

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))
        faker = Faker()
        for _ in range(150):

            self.application_type = faker.random_element(
                elements=(
                    PermanentResidenceApplicationTypeEnum.PERMANENT_RESIDENCE_ONLY.value,
                    PermanentResidenceApplicationTypeEnum.PERMANENT_RESIDENCE_10_YEARS.value,
                )
            )
            with atomic():
                app, version = self.create_basic_data()

                PermanentResidence.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    investor_contribution=self.faker.text(),
                    employee_contribution=self.faker.text(),
                    any_other_resident=self.faker.name(),
                    violated_terms_before=self.faker.text(),
                    preferred_method_comm=self.faker.text(),
                    language=self.faker.text(),
                    spouse_applying_residence=self.faker.text(),
                    prohibited_in_botswana=self.faker.text(),
                    reasons_prohibited=self.faker.text(),
                    imprisonment_any_country=self.faker.text(),
                    reasons_imprisonment=self.faker.text(),
                    permit_reasons=self.faker.text(),
                    period_when_required=self.faker.date_this_century(),
                    take_up_occupation=self.faker.text(),
                    application_reason=self.faker.text(),
                    application_reason_other=self.faker.text(),
                    application_status=self.faker.text(),
                )

                self.stdout.write(
                    self.style.SUCCESS("Successfully populated blue card data")
                )

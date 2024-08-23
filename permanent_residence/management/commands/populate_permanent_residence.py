from django.db.transaction import atomic
from faker import Faker

from app.utils import ApplicationProcesses
from lichois.management.base_command import CustomBaseCommand
from permanent_residence.enums import PermanentResidenceApplicationTypeEnum
from permanent_residence.models.permanent_residence import PermanentResidence


class Command(CustomBaseCommand):
    help = "Populate data for Populate data for Blue card service"
    process_name = ApplicationProcesses.PERMANENT_RESIDENCE.value
    application_type = (
        PermanentResidenceApplicationTypeEnum.PERMANENT_RESIDENCE_ONLY.value,
        PermanentResidenceApplicationTypeEnum.PERMANENT_RESIDENCE_10_YEARS.value,
    )

    def handle(self, *args, **options):
        faker = Faker()
        self.stdout.write(self.style.SUCCESS(f"Process name {self.process_name}"))

        for _ in range(150):

            with atomic():
                app, version = self.create_basic_data()

                PermanentResidence.objects.get_or_create(
                    application_version=version,
                    document_number=app.application_document.document_number,
                    investor_contribution=faker.text(),
                    employee_contribution=faker.text(),
                    any_other_resident=faker.name(),
                    violated_terms_before=faker.text(),
                    preferred_method_comm=faker.text(),
                    language=faker.text(),
                    spouse_applying_residence=faker.text(),
                    prohibited_in_botswana=faker.text(),
                    reasons_prohibited=faker.text(),
                    imprisonment_any_country=faker.text(),
                    reasons_imprisonment=faker.text(),
                    permit_reasons=faker.text(),
                    period_when_required=faker.date_this_century(),
                    take_up_occupation=faker.text(),
                    application_reason=faker.text(),
                    application_reason_other=faker.text(),
                    application_status=faker.text(),
                )

                self.stdout.write(
                    self.style.SUCCESS("Successfully populated blue card data")
                )

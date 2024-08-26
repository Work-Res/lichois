from django.db.transaction import atomic

from datetime import date
from django.core.management.base import BaseCommand

from citizenship.utils import CitizenshipProcessEnum
from gazette.models import Batch, BatchApplication
from lichois.management.base_command import CustomBaseCommand
from identifier.simple_identifier import SimpleIdentifier


class Command(CustomBaseCommand):
    help = 'Start listening to RabbitMQ queues'
    process_name = CitizenshipProcessEnum.RENUNCIATION.value
    application_type = CitizenshipProcessEnum.RENUNCIATION.value

    def handle(self, *args, **options):
        apps = []
        for _ in range(300):

            with atomic():
                app, version = self.create_basic_data()

                self.stdout.write(
                    self.style.SUCCESS("Successfully populated renunciation data")
                )
                apps.append(app)
        count = Batch.objects.all().count()
        count = count + 1
        batch = Batch.objects.create(
            identifier=self.identifier(),
            title=f"Batch {count}",
            description=f"Gazette List {count}",
            status="OPEN",
            submission_date=date.today()
        )
        for application in apps:
            BatchApplication.objects.create(
                application=application, batch=batch
            )
        self.stdout.write(self.style.SUCCESS("Successfully populated data"))

    def identifier(self):
        today = date.today()
        date_string = today.strftime('%d%m%Y')
        simple = SimpleIdentifier(identifier_prefix="DB", address_code=date_string[-6:])
        return simple.identifier

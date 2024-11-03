import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date

from app_checklist.models import SystemParameterPermitRenewalPeriod


class Command(BaseCommand):
    help = "Create or update SystemParameterPermitRenewalPeriod with specified values."

    def add_arguments(self, parser):
        parser.add_argument(
            '--percent',
            type=Decimal,
            default=Decimal('0.25'),
            help="Specify the percentage as a decimal (e.g., 0.25 for 25%).",
        )
        parser.add_argument(
            '--application_type',
            type=str,
            required=True,
            help="Specify the application type.",
        )
        parser.add_argument(
            '--valid_from',
            type=str,
            help="Specify the start date (YYYY-MM-DD format).",
        )
        parser.add_argument(
            '--valid_to',
            type=str,
            help="Specify the end date (YYYY-MM-DD format).",
        )

    def handle(self, *args, **options):
        # Retrieve options
        percent = options['percent']
        application_type = options['application_type']
        valid_from = parse_date(options['valid_from']) if options['valid_from'] else datetime.date.today()
        valid_to = parse_date(options['valid_to'])

        # Create or update the record
        renewal_period, created = SystemParameterPermitRenewalPeriod.objects.update_or_create(
            application_type=application_type,
            defaults={
                'percent': percent,
                'valid_from': valid_from,
                'valid_to': valid_to,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(
                f"Created new SystemParameterPermitRenewalPeriod for application type '{application_type}'"
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Updated SystemParameterPermitRenewalPeriod for application type '{application_type}'"
            ))

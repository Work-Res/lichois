from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import ApplicationDecisionType


class Command(BaseCommand):
    help = "Create objects of DecisionType model"

    def handle(self, *args, **kwargs):
        decision_types = [
            {
                "code": "ACCEPTED",
                "name": "ACCEPTED",
                "process_types": "",
                "valid_from": timezone.now(),
                "valid_to": None,
            },
            {
                "code": "REJECTED",
                "name": "REJECTED",
                "process_types": "",
                "valid_from": timezone.now(),
                "valid_to": None,
            },
        ]

        for dt in decision_types:
            ApplicationDecisionType.objects.create(**dt)
            self.stdout.write(self.style.SUCCESS(f"Created DecisionType: {dt['name']}"))

        self.stdout.write(
            self.style.SUCCESS("Successfully created all DecisionType objects")
        )

import os

from django.core.management.base import BaseCommand
from app_checklist.models import Holiday

from app_checklist.utils import ReadJSON


class Command(BaseCommand):
    help = 'Import holidays from JSON'

    def handle(self, *args, **kwargs):
        # Define the location of the JSON file
        location = os.path.join("app_checklist", "data", "holidays", "2024.json")

        # Read the JSON data
        data = ReadJSON(location).json_data()

        # Loop over each entry in the holiday list
        for data in data['holidays']:
            Holiday.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'Created new holiday for {data}'))

        self.stdout.write(self.style.SUCCESS(f'All holidays were created.'))

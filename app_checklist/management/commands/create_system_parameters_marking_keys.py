import os
from django.core.management.base import BaseCommand
from app_checklist.models import SystemParameter, SystemParameterMarkingKey

from app_checklist.utils import ReadJSON  # Assuming ReadJSON is a custom utility to read the JSON


class Command(BaseCommand):
    help = 'Import system parameters from JSON'

    def handle(self, *args, **kwargs):
        # Define the location of the JSON file
        location = os.path.join("app_checklist", "data", "system_parameters_marking_keys", "parameters.json")

        # Read the JSON data
        data = ReadJSON(location).json_data()

        # Loop over each entry in the system_parameters list
        for param in data['system_parameters']:
            # Some entries have multiple application types separated by commas, handle them
            marking_code = param['code']

            # Use update_or_create to either update an existing record or create a new one
            system_param, created = SystemParameterMarkingKey.objects.update_or_create(
                code=marking_code,
                defaults={
                    'pass_mark_in_percent': param['pass_mark_in_percent'],
                    'total_marks': param['total_marks'],
                    'valid_from': param['valid_from'],
                    'valid_to': param['valid_to']
                }
            )

            # Provide feedback in the console
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created new system parameter for {marking_code}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated system parameter for {marking_code}'))

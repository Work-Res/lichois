import os
from django.core.management.base import BaseCommand
from app_checklist.models import SystemParameter

from app_checklist.utils import ReadJSON  # Assuming ReadJSON is a custom utility to read the JSON


class Command(BaseCommand):
    help = 'Import system parameters from JSON'

    def handle(self, *args, **kwargs):
        # Define the location of the JSON file
        location = os.path.join("app_checklist", "data", "system_parameters", "parameters.json")

        # Read the JSON data
        data = ReadJSON(location).json_data()

        # Loop over each entry in the system_parameters list
        for param in data['system_parameters']:
            # Some entries have multiple application types separated by commas, handle them
            application_types = param['application_type'].split(", ")
            self.stdout.write(self.style.WARNING(f'{application_types}'))

            for application_type_str in application_types:
                # Attempt to find the corresponding enum value if using an enum, otherwise use the string directly
                try:
                    # Assuming CitizenshipProcessEnum maps to the correct enum for application types
                    application_type_enum_value = application_type_str
                except KeyError:
                    self.stdout.write(self.style.WARNING(f'Skipping unknown application_type: {application_type_str}'))
                    continue

                # Use update_or_create to either update an existing record or create a new one
                system_param, created = SystemParameter.objects.update_or_create(
                    application_type=application_type_enum_value,
                    defaults={
                        'duration_type': param['duration_type'],
                        'duration': param['duration'],
                        'valid_from': param['valid_from'],
                        'valid_to': param['valid_to']
                    }
                )

                # Provide feedback in the console
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new system parameter for {application_type_str}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated system parameter for {application_type_str}'))

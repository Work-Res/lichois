from django.core.management.base import BaseCommand

from app.models import ApplicationStatus
from app.utils import statuses
from citizenship.utils import CitizenshipProcessEnum


class Command(BaseCommand):
    help = 'Update ApplicationStatus records based on your criteria'

    def handle(self, *args, **options):

        for status in statuses:
            code = status.get("code")
            # Assuming 'status' contains other fields that you want to create/update the object with
            print(f"Attempting to create code: {code}")
            application_status, created = ApplicationStatus.objects.get_or_create(
                code__iexact=code,  # Use code to find the existing object
                defaults=status  # Use 'status' as the defaults if creating a new object
            )
            if created:
                print(f"Created new ApplicationStatus with code {code}")
            else:
                processes = application_status.processes.split(',')
                for process in CitizenshipProcessEnum:
                    if not process.value in processes:
                        application_status.processes = f"{application_status.processes},{process}"
                        application_status.save()
                        self.stdout.write(
                            self.style.SUCCESS(f'Updated the application status, added {process.value}'))
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(f'Already udated the application status, for {process.value}'))
                print(f"Found existing ApplicationStatus with code {code}")

        # Log results
        self.stdout.write(self.style.SUCCESS(f'Successfully updated application status for citizenship'))

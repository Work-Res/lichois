from calendar import c
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.apps import apps


class Command(BaseCommand):
    help = "Run makemigrations for all valid apps listed in INSTALLED_APPS."

    def handle(self, *args, **kwargs):
        installed_apps = settings.INSTALLED_APPS

        for app_name in installed_apps:
            try:
                # Get the app config to obtain the correct label
                x = app_name.split(".")[0]
                app_config = apps.get_app_config(x)
                app_label = app_config.label
            except LookupError:
                # Skip non-app entries or invalid entries
                self.stdout.write(
                    self.style.WARNING(f"Skipping invalid app entry: {app_name}")
                )
                continue

            self.stdout.write(f"Making migrations for app: {app_label}")
            try:
                call_command("makemigrations", app_label)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to make migrations for {app_label}: {e}")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully made migrations for {app_label}")
                )
                call_command("migrate", app_label)

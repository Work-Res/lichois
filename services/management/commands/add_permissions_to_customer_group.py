from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

class Command(BaseCommand):
    help = 'Add model permissions (add, change, view) to the customer group for all models'

    def handle(self, *args, **kwargs):
        # Get or create the customer group
        customer_group, created = Group.objects.get_or_create(name='customer')

        # Iterate through all models in all installed apps
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                # Get the permissions for the model
                model_name = model._meta.model_name
                app_label = model._meta.app_label
                permissions = [
                    f'add_{model_name}',
                    f'change_{model_name}',
                    f'view_{model_name}',
                ]

                # Add the permissions to the customer group
                for perm in permissions:
                    try:
                        permission = Permission.objects.get(codename=perm, content_type__app_label=app_label)
                        customer_group.permissions.add(permission)
                        self.stdout.write(self.style.SUCCESS(f'Added {perm} permission for {model_name} to customer group'))
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'Permission {perm} does not exist for {model_name}'))

        self.stdout.write(self.style.SUCCESS('Successfully added permissions to customer group'))
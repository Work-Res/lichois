import os
from django.apps import AppConfig as BaseAppConfig

class AppConfig(BaseAppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_production"

    def ready(self):
        from .classes import (
            ServiceLoader,
            ServiceRegistry,
        )

        # Initialize the service registry
        service_registry = ServiceRegistry()

        services_directory = os.path.join(os.path.dirname(__file__), "services")

        # Load services from the 'services' directory
        service_loader = ServiceLoader(services_directory, service_registry)
        service_loader.load_services()

        # Store the service registry in the app config for later use
        self.service_registry = service_registry
        from .signals import create_production_permit_record

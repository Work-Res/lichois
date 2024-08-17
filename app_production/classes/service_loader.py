import os
import importlib

from app_production.services.permit_production_service import PermitProductionService

"""
    ServiceLoader is a class that loads all services from a specified directory,
    registers them in a service registry using the application type as the key,
    and stores the service registry in the app config for later use.

    The ServiceLoader class takes two parameters: service_directory and registry.
    The service_directory parameter specifies the directory where the services are located,
    and the registry parameter is an instance of the ServiceRegistry class where the services will be registered.
"""


class ServiceLoader:
    def __init__(self, service_directory, registry):
        self.service_directory = service_directory
        self.registry = registry

    def load_services(self):
        """
        Load all services from the specified directory and register them
        in the service registry using the application type as the key.
        """
        for filename in os.listdir(self.service_directory):
            if filename.endswith(".py") and filename != "__init__.py":
                # Extract the module name from the filename
                module_name = filename[:-3]
                # Construct the module path using dot notation
                module_path = f"app_production.services.{module_name}"

                try:
                    # Import the module dynamically
                    module = importlib.import_module(module_path)
                except TypeError as e:
                    if "the 'package' argument is required" in str(e):
                        # Provide the package argument for relative import
                        package = self.service_directory.replace(os.sep, ".")
                        module = importlib.import_module(module_path, package=package)
                    else:
                        raise

                # Register all classes in the module
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if isinstance(attribute, type) and issubclass(
                        attribute, PermitProductionService
                    ):  # Check if it's a class
                        # Check if the class has an application_type attribute
                        if hasattr(attribute, "process_name"):
                            process_name = getattr(attribute, "process_name")
                            self.registry.register(process_name, attribute)

                        else:
                            print(
                                f"Warning: Service {attribute.__name__} does not have an process_name attribute."
                            )

import logging


# classes/service_registry.py
class ServiceRegistry:
    def __init__(self):
        """
        Initialize an empty service registry.
        """
        self._registry = {}
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARNING)

    def register(self, service_name, service_class):
        """
        Register a service class with a given name.

        :param service_name: Name of the service
        :param service_class: Class of the service
        """
        self._registry[service_name] = service_class
        self.logger.warn(f"Registered service: {service_name} - {service_class}")

    def get_service(self, service_name):
        """
        Retrieve a service class by its name.

        :param service_name: Name of the service
        :return: Service class or None if not found
        """
        return self._registry.get(service_name)

    def get_all_services(self):
        """
        Retrieve all registered services.

        :return: Dictionary of all registered services
        """
        return self._registry

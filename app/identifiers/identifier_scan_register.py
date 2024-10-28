import importlib
import pkgutil
import logging
from django.apps import apps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IdentifierScanRegister:
    def __init__(self):
        self.registered_identifier_config_classes = {}

    def scan_and_register_identifier_config_classes(
        self, key_method_name="process_name"
    ):
        logger.info("Starting to scan and register classes...")

        for app_config in apps.get_app_configs():
            self._scan_app(app_config, key_method_name)

    def _scan_app(self, app_config, key_method_name):
        app_module = app_config.module

        for _, module_name, is_pkg in pkgutil.iter_modules(app_module.__path__):
            if module_name == "identifier_config":
                full_module_name = f"{app_module.__name__}.{module_name}"
                self._import_and_register_module(full_module_name, key_method_name)
                self._scan_submodules(full_module_name, key_method_name)

    def _scan_submodules(self, module_name, key_method_name):
        try:
            module = importlib.import_module(module_name)
            for _, submodule_name, is_pkg in pkgutil.iter_modules(module.__path__):
                full_submodule_name = f"{module_name}.{submodule_name}"
                self._import_and_register_module(full_submodule_name, key_method_name)
        except ImportError as e:
            logger.error(f"Failed to import module {module_name}: {e}")

    def _import_and_register_module(self, module_name, key_method_name):
        try:
            module = importlib.import_module(module_name)
            self._register_classes_in_module(module, key_method_name)
        except ImportError as e:
            logger.error(f"Failed to import module {module_name}: {e}")

    def _register_classes_in_module(self, module, key_method_name):
        for name, obj in module.__dict__.items():
            if isinstance(obj, type):
                self._register_class(obj, key_method_name)

    def _register_class(self, cls, key_method_name):
        key_method = getattr(cls, key_method_name, None)
        if callable(key_method):
            key = key_method()
            self.registered_identifier_config_classes[key] = cls

    def get_registered_class(self, key):
        return self.registered_identifier_config_classes.get(key)


registrar = IdentifierScanRegister()

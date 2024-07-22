from django.test import TestCase
from app.identifiers import IdentifierScanRegister
from citizenship.utils import CitizenshipProcessEnum


class IdentifierScanRegisterTest(TestCase):

    def setUp(self):
        self.registrar = IdentifierScanRegister()

    def test_get_registered_class_when_process_name_exists(self):
        """Check if the process name is registered."""
        self.registrar.scan_and_register_identifier_config_classes(
            key_method_name="process_name"
        )
        process_name = CitizenshipProcessEnum.RENUNCIATION.value
        citizenship_enunciation_cls = self.registrar.get_registered_class(process_name)
        self.assertIsNotNone(citizenship_enunciation_cls)
        self.assertTrue(
            process_name in self.registrar.registered_identifier_config_classes
        )

    def test_get_registered_class_when_process_name_not_registered(self):
        """Check if the process name is registered."""
        self.registrar.scan_and_register_identifier_config_classes(
            key_method_name="process_name"
        )
        process_name = "citizenship_renunciation_invalid"
        citizenship_enunciation_cls = self.registrar.get_registered_class(process_name)
        self.assertIsNone(citizenship_enunciation_cls)
        self.assertFalse(
            process_name in self.registrar.registered_identifier_config_classes
        )

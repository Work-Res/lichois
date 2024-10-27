# import os
#
# from django.test import TestCase
# from django.core.exceptions import ObjectDoesNotExist
#
# from ..classes.production import FetchRequiredDataForProduction
#
#
# class TestFetchRequiredDataForProduction(TestCase):
#
#     def setUp(self) -> None:
#         self.document_number = "test-document"
#         file_name = "work_resident_permit_only.json"
#         output_file = os.path.join(
#             os.getcwd(), "workresidentpermit", "classes", "production", "configuration", file_name)
#         self.fetch_data_util = FetchRequiredDataForProduction(configuration_file_name=output_file,
#                                                          document_number=self.document_number)
#
#     def test_read_configuration(self):
#         """Check if the configuration can be read from the configuration."""
#         fetched_config = self.fetch_data_util .read_configuration()
#         self.assertIsNotNone(fetched_config)
#
#     def test_read_configuration_expected_data(self):
#         """Checks if configuration content is what is expected.
#         """
#         is_model_available = "models" in self.fetch_data_util.read_configuration()
#         self.assertTrue(is_model_available)
#
#         model_fields = self.fetch_data_util.read_configuration().get("models")
#         self.assertGreater(len(model_fields), 0)
#
#     def test_get_data_no_results(self):
#         """Checks if the method will return empty list.
#         """
#         with self.assertRaises(ObjectDoesNotExist) as context:
#             self.fetch_data_util.get_data()
#         self.assertEqual(str(context.exception), "Object with document number test-document not found in person")
#         print(str(context.exception))

# import os Fixme Refactor to carter to prepoluation
#
# from django.test import TestCase
#
# from faker import Faker
#
# from app_checklist.classes import CreateChecklistService
# from app_personal_details.models import Person
# from app.utils import statuses, ApplicationProcesses
#
# from ..classes import PrePopulationService, PrepopulationConfiguration
# from ..api import NewApplicationDTO
#
# from app.models import ApplicationStatus
#
#
# class TestPrepupolationService(TestCase):
#
#     def setUp(self):
#
#         file_name = "attachment_documents.json"
#         output_file = os.path.join(os.getcwd(), "app_checklist", "data", file_name)
#         create = CreateChecklistService()
#         create.create(file_location=output_file)
#
#         faker = Faker()
#
#         for status in statuses:
#             ApplicationStatus.objects.create(
#                 **status
#             )
#
#         self.new_app = NewApplicationDTO(
#             process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
#             applicant_identifier='317918515',
#             status=ApplicationStatuses.NEW.value,
#             dob="06101990",
#             work_place="01",
#             full_name="Test test")
#
#         self.create_new = CreateNewApplicationService(new_application=self.new_app)
#
#         self.application_version = self.create_new.create()
#         app = self.application_version.application
#
#         Person.objects.get_or_create(
#             document_number=app.application_document.document_number,
#             application_version=None,
#             first_name=faker.unique.first_name(),
#             last_name=faker.unique.last_name(),
#             dob=faker.date_of_birth(minimum_age=18, maximum_age=65),
#             middle_name=faker.first_name(),
#             marital_status=faker.random_element(elements=('single', 'married', 'divorced')),
#             country_birth=faker.country(),
#             place_birth=faker.city(),
#             gender=faker.random_element(elements=('male', 'female')),
#             occupation=faker.job(),
#             qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd'))
#         )
#
#     def test_get_configuration(self):
#         """ Test if the prepopulation class can read prepopulatio configuration for the specified process name.
#         """
#         file_name = "work_permit.json"
#         configuration_location = os.path.join(os.getcwd(), "app_checklist", "data", "prepopulation", file_name)
#         pre = PrePopulationService(configuration_location=configuration_location)
#         pre.configuration()
#         self.assertIsNotNone(pre.prepopulation_configuration)
#         self.assertIsInstance(pre.prepopulation_configuration, PrepopulationConfiguration)
#
#     def test_get_configuration_when_valid(self):
#         """ Test if the prepopulation class can read prepopulation correctly.
#         """
#         file_name = "work_permit.json"
#         configuration_location = os.path.join(os.getcwd(), "app_checklist", "data", "prepopulation", file_name)
#         pre = PrePopulationService(configuration_location=configuration_location)
#         pre.configuration()
#         self.assertIsNotNone(pre.prepopulation_configuration)
#         print("pre.prepopulation_configuration ", pre.prepopulation_configuration)
#         self.assertEqual(2, len(pre.prepopulation_configuration.models))
#
#     def test_get_configuration_when_all_models_configured_are_valid(self):
#         """ Test if the prepopulation class when configured models should be valid.
#         """
#         file_name = "work_permit.json"
#         configuration_location = os.path.join(os.getcwd(), "app_checklist", "data", "prepopulation", file_name)
#         pre = PrePopulationService(configuration_location=configuration_location, filter_data={"document_number": "WR000001"})
#
#         self.assertTrue(pre.prepupoluate())

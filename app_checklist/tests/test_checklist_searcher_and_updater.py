from django.test import TestCase

from django.apps import apps
from app_checklist.apps import AppChecklistConfig

from ..classes import ChecklistSearcherAndUpdater
from ..models import ChecklistClassifierItem, Classifier


class TestChecklistSearcherAndUpdater(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app_config = apps.get_app_config('app_checklist')
        if isinstance(app_config, AppChecklistConfig):
            app_config.ready()

    def test_search_json_files_in_directories(self):
        searcher = ChecklistSearcherAndUpdater(target_directory_name="checklist")
        searcher.search_directories_in_apps()
        searcher.search_json_files_in_directories()
        data = ['renunciation_attachment_documents.json']
        found_files = []
        for f, d in searcher.json_files.items():
            found_files.extend(d)
        for expected_file in data:
            is_found = any([expected_file in s for s in found_files])
            self.assertTrue(is_found)

    def test_create_checklist_count_config_checklist(self):
        # Fixme Fix the test below to create checklist records..
        checklist = ChecklistClassifierItem.objects.filter(
            application_type__icontains='CITIZENSHIP_RENUNCIATION')
        self.assertEqual(8, checklist.count())

    def test_create_workflow_config(self):
        # Fixme Fix the test below to create checklist records..
        # searcher = ChecklistSearcherAndUpdater(target_directory_name="workflow")
        # searcher.update_workflow()
        workflows = Classifier.objects.filter(code='CITIZENSHIP_RENUNCIATION')
        self.assertGreater(workflows.count(), 0)

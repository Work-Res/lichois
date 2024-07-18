from django.test import TestCase

from ..classes import ChecklistSearcherAndUpdater
from ..models import ChecklistClassifier, ChecklistClassifierItem


class TestChecklistSearcherAndUpdater(TestCase):

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
        searcher = ChecklistSearcherAndUpdater(target_directory_name="checklist")
        searcher.update_checklist()
        checklist = ChecklistClassifierItem.objects.filter(
            application_type__icontains='CITIZENSHIP_RENUNCIATION')
        self.assertEqual(7, checklist.count())

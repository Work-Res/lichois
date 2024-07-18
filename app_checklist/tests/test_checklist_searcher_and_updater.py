from django.test import TestCase

from ..classes import ChecklistSearcherAndUpdater


class TestChecklistSearcherAndUpdater(TestCase):

    def test_search_json_files_in_directories(self):
        searcher = ChecklistSearcherAndUpdater(target_directory_name="checklist")
        searcher.search_directories_in_apps()
        searcher.search_json_files_in_directories()
        data = ['/Users/tsetsiba/MY_PROJECTS/development/lichois/app_checklist/data/checklist/citizenship.json',
                '/Users/tsetsiba/MY_PROJECTS/development/lichois/app_checklist/data/checklist/a'
                'ttachment_documents.json',
                '/Users/tsetsiba/MY_PROJECTS/development/lichois/workresidentpermit/data/checklist'
                '/sample_attachment_documents.json',
                '/Users/tsetsiba/MY_PROJECTS/development/lichois/citizenship/data/checklist'
                '/renunciation_attachment_documents.json']
        found_files = []
        for f, d in searcher.json_files.items():
            found_files.extend(d)
        for expected_file in data:
            is_found = expected_file in found_files
            self.assertTrue(is_found)

    def test_create_checklist(self):
        # Fixme Fix the test below to create checklist records..
        searcher = ChecklistSearcherAndUpdater(target_directory_name="checklist")
        searcher.update_checklist()

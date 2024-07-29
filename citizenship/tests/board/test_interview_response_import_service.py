import os
import tempfile
from django.test import TestCase
from unittest.mock import patch, mock_open

from citizenship.service.board import InterviewResponseImportService


class TestInterviewResponseImportService(TestCase):

    def setUp(self):
        # Create a temporary CSV file for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = os.path.join(self.temp_dir.name, 'test.csv')
        self.csv_content = """text,category,marks_range
"Setswana or any other local language","Proficiency",0-10
"Level of Education","Proficiency",0-10
"""
        with open(self.csv_path, 'w') as f:
            f.write(self.csv_content)

    def tearDown(self):
        # Cleanup temporary directory and files
        self.temp_dir.cleanup()

    def test_read_csv_success(self):
        service = InterviewResponseImportService(self.csv_path)
        service.read_csv()
        self.assertEqual(len(service.data), 2)
        self.assertEqual(service.data[0]['text'], 'Setswana or any other local language')

    def test_file_not_found(self):
        service = InterviewResponseImportService('non_existent_file.csv')
        with self.assertLogs('your_app.services', level='ERROR') as cm:
            service.read_csv()
            self.assertIn('File not found: non_existent_file.csv', cm.output[0])

    @patch('builtins.open', new_callable=mock_open, read_data='invalid data')
    def test_unexpected_error(self, mock_file):
        service = InterviewResponseImportService(self.csv_path)
        with self.assertLogs('your_app.services', level='ERROR') as cm:
            service.read_csv()
            self.assertIn('Unexpected error reading file', cm.output[0])

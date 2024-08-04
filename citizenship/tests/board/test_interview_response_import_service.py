import os
import tempfile
from django.test import TestCase

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


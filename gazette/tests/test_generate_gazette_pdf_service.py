import os
import docx

from django.conf import settings


from gazette.service import GenerateGazettePDFService

from .base_setup import BaseSetup


class TestGenerateGazettePDFService(BaseSetup):

    def setUp(self):
        self.data = [
            ["ID", "Fullname", "Location", "Document Number"],
            ["1", "Test test", "Ranaka", "RZn0001"],
            ["2", "Bryce Sets", "Kanye", "R2000001"],
            ["3", "Laim Kgathi", "Moshupa", "R4000333"]
        ]

        self.word_file_path = os.path.join(settings.MEDIA_ROOT, "test_application_1.docx")
        self.pdf_file_path = os.path.join(settings.MEDIA_ROOT, "test_applications_1.pdf")
        self.service = GenerateGazettePDFService(self.data, self.word_file_path, self.pdf_file_path)

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.word_file_path):
            os.remove(self.word_file_path)
        if os.path.exists(self.pdf_file_path):
            os.remove(self.pdf_file_path)

    def test_create_word_document(self):
        self.service.create_word_document()
        # Ensure the Word document is created
        self.assertTrue(os.path.exists(self.word_file_path))

        # Additional checks for document content
        doc = docx.Document(self.word_file_path)
        self.assertEqual(doc.paragraphs[0].text, "Gazette List")
        table = doc.tables[0]
        self.assertEqual(len(table.rows), 4)  # 1 header row + 3 data rows
        self.assertEqual(table.cell(0, 0).text, "ID")
        self.assertEqual(table.cell(1, 0).text, "1")
        self.assertEqual(table.cell(2, 1).text, "Bryce Sets")
        self.assertEqual(table.cell(3, 2).text, "Moshupa")

    def test_convert_to_pdf(self):
        self.service.create_word_document()
        self.service.convert_to_pdf()
        # Ensure the PDF document is created
        self.assertTrue(os.path.exists(self.pdf_file_path))

    def test_generate_pdf(self):
        self.service.generate_pdf()
        # Ensure both Word and PDF documents are created
        self.assertTrue(os.path.exists(self.word_file_path))
        self.assertTrue(os.path.exists(self.pdf_file_path))

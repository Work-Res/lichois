import os

from django.test import TestCase
from datetime import date

from app_production.handlers.common import ProductionConfig, GenericProductionContext
from app_production.handlers.postsave.upload_document_production_handler import (
    UploadDocumentProductionHandler,
)
from app_production.models import ProductionAttachmentDocument


class TravelWorkTemplate(TestCase):

    def setUp(self):
        self.context = {
            "surname": "Letsile Tebogo",
            "middle_name": "Schoolboy",
            "place_of_birth": "Kanye",
            "document_type": "travel_certificate",
            "dob": "06/10/2003",
            "place_of_birth": "Kanye",
            "present_nationality": "Motswana",
            "original_home_address": "Ntsweng, Kanye",
            "mother_full_names": "Seritiwa Letsile",
            "mother_full_address": "Ntsweng, Kanye",
            "chief": "Thelekelo, Karabo",
            "country_of_origin": "Botswana",
            "original_home_address": "",
            "father_full_names": "",
            "father_full_address": "",
            "names_of_other_living_relatives": "",
            "full_address_of_relative": "",
            "kraal_head_or_headman": "",
            "clan": "",
            "document_number": "TRC/010000",
            "date": "09/08/2024",
            "original_home_address": "",
            "year": "2024",
        }

    def test_populate_travel_certificate_template(self):
        """Check if the travel certificate is create as per configuration"""
        self.context = {key: value.upper() for key, value in self.context.items()}
        template_path = os.path.join(
            "travel",
            "data",
            "production",
            "templates",
            "travel_certificate_template.docx",
        )
        document_output_path_word = os.path.join(
            "travel", "tests", "outputs", "travel_certificate_output.docx"
        )
        document_output_path_pdf = os.path.join(
            "travel", "tests", "outputs", "travel_certificate_output.pdf"
        )

        config = ProductionConfig(
            template_path=template_path,
            document_output_path=document_output_path_word,
            document_output_path_pdf=document_output_path_pdf,
            is_required=True,
        )
        context = GenericProductionContext()
        context.context = lambda: self.context

        handler = UploadDocumentProductionHandler()
        handler.execute(config_cls=config, production_context=context)
        production_attachments = ProductionAttachmentDocument.objects.get(
            document_number="TRC/010000"
        )

        self.assertIsNotNone(production_attachments)

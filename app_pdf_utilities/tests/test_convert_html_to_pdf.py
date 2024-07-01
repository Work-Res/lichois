import os

from datetime import date
from django.conf import settings
from django.test import TestCase

from app_pdf_utilities.classes import ConvertHtmlToPdf

from .invoice_sample_html import invoice_html_content
from .multiple_html_pages import mutiple_pages
from .sample_static_frame import frame
from .certificate import  html

from .data_for_tests import data


class TestConvertHtmlToPDF(TestCase):

    def test_convert_html_to_pdf(self):
        file_name = "test.pdf"
        output_file = os.path.join(os.getcwd(), "app_pdf_utilities", "tests", "output_results", file_name)
        source_html = "<html><body><p>To PDF or not to PDF</p></body></html>"

        pdf_util = ConvertHtmlToPdf(source_html=source_html, output_filename=output_file)
        pdf_util.convert_plain_html_to_pdf()

    def test_convert_html_to_pdf_invoice_sample(self):
        file_name = "invoice_sample.pdf"
        output_file = os.path.join(os.getcwd(), "app_pdf_utilities", "tests", "output_results", file_name)
        data = {
            'date': date.today(),
            'amount': 40.99,
            'customer_name': 'Test Test',
            'invoice_number': 1233434,
        }

        converter = ConvertHtmlToPdf()
        status = converter.convert_html_to_pdf(context=data, html_content=invoice_html_content,
                                               file_location=output_file)
        assert status == False

    def test_convert_html_to_pdf_multiple_pages(self):
        file_name = "multiple_pages.pdf"
        output_file = os.path.join(os.getcwd(), "app_pdf_utilities", "tests", "output_results", file_name)

        converter = ConvertHtmlToPdf()
        status = converter.convert_html_to_pdf(context=None, html_content=mutiple_pages,
                                               file_location=output_file)
        assert status == False

    def test_convert_html_to_pdf_static_frame(self):
        file_name = "multiple_static_pages.pdf"
        output_file = os.path.join(os.getcwd(), "app_pdf_utilities", "tests", "output_results", file_name)

        converter = ConvertHtmlToPdf()
        context = {
            "image_url": os.path.join(settings.MEDIA_ROOT, "logo.png"),
            "data": data
        }
        status = converter.convert_html_to_pdf(context=context, html_content=frame,
                                               file_location=output_file)
        assert status == False

    def test_production_template_work_resident(self):
        file_name = "production.pdf"
        output_file = os.path.join(os.getcwd(), "app_pdf_utilities", "tests", "output_results", file_name)

        converter = ConvertHtmlToPdf()

        context = {'first_name': 'Sharon', 'last_name': 'Tyler', 'gender': 'male', 'dob': '1990-01-01',
                   'passport_number': '948645313', 'place_issue': 'Gaborone', 'permit_no': 'test',
                   'date_issued': "2024-01-01", 'date_expiry': '2025-01-01',
                   'permit_type': 'WORK_RESIDENT_PERMIT', 'security_number': '303919388',
                   'passport_photo': os.path.join(settings.MEDIA_ROOT, "img.png"),
                   'generated_barcode': os.path.join(settings.MEDIA_ROOT, "logo.png"),
                   'barcode': os.path.join(settings.MEDIA_ROOT, "barcode.png")}

        status = converter.convert_html_to_pdf(
            context=context,
            template_path="pdf/work-permit.html",
            file_location=output_file)

    def test_travel_certificate(self):
        file_name = "travel_certificate.pdf"
        output_file = os.path.join(os.getcwd(), "app_pdf_utilities", "tests", "output_results", file_name)

        converter = ConvertHtmlToPdf()
        context = {
            "image_url": os.path.join(settings.MEDIA_ROOT, "logo.png"),
            "data": data
        }

        status = converter.convert_html_to_pdf(context=context, html_content=html,
                                               file_location=output_file)
        assert status == False

    # def test_pdf(self):
    #     file_name = "production.pdf"
    #     output_file = os.path.join(os.getcwd(), "app_pdf_utilities", "tests", "output_results", file_name)
    #
    #     converter = ConvertHtmlToPdf()
    #
    #     context = {'first_name': 'Sharon', 'last_name': 'Tyler', 'gender': 'male', 'dob': '1990-01-01',
    #                'passport_number': '948645313', 'place_issue': 'Gaborone', 'permit_no': 'test',
    #                'date_issued': "2024-01-01", 'date_expiry': '2025-01-01',
    #                'permit_type': 'WORK_RESIDENT_PERMIT', 'security_number': '303919388'}
    #
    #     status = converter.convert_html_to_pdf(
    #         context=context,
    #         template_path="pdf/work-permit.html",
    #         file_location=output_file)

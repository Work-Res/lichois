import os


from datetime import date
from django.conf import settings

from app_pdf_utilities.classes import ConvertHtmlToPdf

from .invoice_sample_html import invoice_html_content
from .multiple_html_pages import mutiple_pages
from .sample_static_frame import frame

from .data_for_tests import data


class TestConvertHtmlToPDF:

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

import os
import uuid

import logging

from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Template, Context

from django.conf import settings


class ConvertHtmlToPdf(object):
    """
    Generates a PDF given source_html, and output_filename. Handles single page PDF and a PDF with multiple pages.
    Attributes:

    """

    def __init__(self, source_html=None, output_filename=None):
        self.logger = logging.getLogger("app_pdf_utilities")
        self.source_html = source_html
        self.output_filename = output_filename

    def to_pdf(self, file_location, html_template):
        pisa_render_status = False
        try:
            with open(file_location, "w+b") as result_file:
                pisa_status = pisa.CreatePDF(html_template, dest=result_file)
                if pisa_status.err is True:
                    pisa_render_status = True
                    self.logger.debug("Failed to create a PDF")
        except Exception as e:
            self.logger.debug(f"Error occurred: {e}")
            pisa_render_status = True
        return pisa_render_status

    def convert_plain_html_to_pdf(self, html_template=None, file_location=None):
        """
        Create PDF from plain HTML without Django variables within the template.
        NB: You this method for single PDF document. ( No support for pagination )
        """
        new_uuid = str(uuid.uuid4())
        file_name = f"{new_uuid}.pdf"
        default = os.path.join(settings.MEDIA_ROOT, "generated_pdf", file_name)
        file_location = file_location or self.output_filename or default
        html_template = html_template or self.source_html
        self.to_pdf(file_location, html_template)

    def convert_html_to_pdf(self, context=None, html_content=None, file_location=None, template_path=None,
                            file_name=None):
        """
        Create PDF from  HTML with Django variables within the template.
        NB: You this method for single PDF document. ( No support for pagination )
        """
        try:
            new_uuid = str(uuid.uuid4())
            _file_name = file_name or f"{new_uuid}.pdf"

            template = get_template(template_path) if template_path else Template(html_content)
            file_location = file_location or self.output_filename or os.path.join(
                settings.MEDIA_ROOT, settings.PDF_FOLDER, _file_name)

            context = Context(context)
            rendered_html = template.render(context)
            pisa_render_status = self.to_pdf(file_location, rendered_html)

            if pisa_render_status:
                self.logger.info("The system generated PDF successfully. ")
            return pisa_render_status
        except Exception as e:
            self.logger.debug("An error occurred while to generate the pdf, Got ", e)

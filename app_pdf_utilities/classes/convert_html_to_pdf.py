import logging

from xhtml2pdf import pisa
from django.template import Template, Context


class ConvertHtmlToPdf(object):
    """
    Generates a PDF given source_html, and output_filename. Handles single page PDF and a PDF with multiple pages.
    Attributes:

    """

    def __init__(self, source_html=None, output_filename=None):
        self.logger = logging.getLogger(__name__)
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
        file_location = file_location or self.output_filename
        html_template = html_template or self.source_html
        self.to_pdf(file_location, html_template)

    def convert_html_to_pdf(self, context=None, html_content=None, file_location=None):
        """
        Create PDF from  HTML with Django variables within the template.
        NB: You this method for single PDF document. ( No support for pagination )
        """
        context = Context(context)
        template = Template(html_content)
        rendered_html = template.render(context)
        return self.to_pdf(file_location, rendered_html)



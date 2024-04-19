from django.views.generic import View

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template


from ..classes import ConvertHtmlToPdf


class GeneratePDFView(View):

    def get(self, request, *args, **kwargs):
        pass
        # template_src = None
        # context_dict = None
        # template = get_template(template_src)
        # html = template.render(context_dict)
        # result = BytesIO()
        # converter = ConvertHtmlToPdf
        # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        # if pdf.err:
        #     return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')
        # return HttpResponse(result.getvalue(), content_type='application/pdf')



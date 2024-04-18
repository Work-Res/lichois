from datetime import datetime

from app_pdf_utilities.renderers import render_to_pdf


def pdf_view(self, request, *args, **kwargs):
    data = {
        'today': datetime.date.today(),
        'amount': 39.99,
        'customer_name': 'Cooper Mann',
        'invoice_number': 1233434,
    }
    return render_to_pdf('pdfs/invoice_sample.html', data)

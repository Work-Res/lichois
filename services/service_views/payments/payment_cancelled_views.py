from django.views.generic import TemplateView

from app_payments.models import Payment
from ..service_application_view_mixin import ServiceApplicationViewMixin


class PaymentsCancelledView(TemplateView, ServiceApplicationViewMixin):

    template_name = 'applications/payments/payment-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(payments=Payment.objects.filter(status='CANCELLED'))
        return context

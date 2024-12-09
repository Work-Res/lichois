from django.views.generic import TemplateView

from app_payments.models import Payment
from ..service_application_view_mixin import ServiceApplicationViewMixin


class PaymentsPaidView(TemplateView, ServiceApplicationViewMixin):

    template_name = 'applications/payments/payment-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(payments=Payment.objects.filter(status='PAID'))

        return context

    def permits(self):
        """Returns a list of all work and res permits.
        """
        return None

    @property
    def new_application(self):
        """Return true if a new application is in progress.
        """
        return True

    @property
    def create_new_application(self):
        """Returns an application number for work and residence permit.
        """
        new_app = self.request.GET.get('new_application', False)
        if new_app:
            # Generate a new application number
            return '123456'

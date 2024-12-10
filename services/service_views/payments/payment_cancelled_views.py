from django.views.generic import TemplateView

from django.db.models import Count

from app_payments.models import Payment
from ..service_application_view_mixin import ServiceApplicationViewMixin


class PaymentsCancelledView(TemplateView, ServiceApplicationViewMixin):

    template_name = 'applications/payments/payment-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the user's non_citizen_identifier
        non_citizen_identifier = getattr(self.request.user, 'non_citizen_identifier', None)

        # Filter payments if non_citizen_identifier is available
        if non_citizen_identifier:
            payments = Payment.objects.filter(non_citizen_identifier=non_citizen_identifier, status="CANCELLED")
        else:
            payments = Payment.objects.none()  # Return an empty queryset if no identifier

        # Group payments by status and count them
        status_counts = (
            payments.values('status')
                .annotate(count=Count('status'))
                .order_by('status')
        )

        # Convert the counts into a dictionary for easier use in templates
        payment_report = {status_count['status']: status_count['count'] for status_count in status_counts}

        # Update context with payments and the report
        context.update(
            payments=payments,
            payment_report=payment_report,
            total=sum(payment_report.values())
        )

        return context

from django.db.models import Count
from django.http import JsonResponse
from django.views import View
from app_payments.models import Payment


class PaymentStatusCountView(View):
    """
    View to return the count of payments grouped by their status.
    """

    def get(self, request, *args, **kwargs):
        # Group payments by status and count them
        status_counts = (
            Payment.objects.values('status')
            .annotate(count=Count('status'))
            .order_by('status')
        )

        # Format the response
        response_data = {status_count['status']: status_count['count'] for status_count in status_counts}
        return JsonResponse(response_data)
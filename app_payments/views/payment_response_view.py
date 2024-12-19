from braces.views import LoginRequiredMixin, CsrfExemptMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from django.views import View
from django.core.exceptions import ValidationError
from app_payments.service import CyberSourceResponseProcessor


class CyberSourceResponseView(CsrfExemptMixin, View):
    """
    Handles the POST response from CyberSource and redirects the user based on the payment decision.
    """

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        response_data = request.POST.dict()  # Convert QueryDict to a regular dictionary

        try:
            processor = CyberSourceResponseProcessor(response_data)
            processor.process_response()

            # Display success message to the user
            messages.success(
                request,
                'Your payment was successfully processed, and continue to submit your application.',
            )
        except ValidationError as e:
            # Display validation error message
            messages.error(request, f"Validation error: {str(e)}")
        except Exception as e:
            # Log unexpected errors and show generic error message
            messages.error(request, f"An unexpected error occurred while processing your payment. {e}")

        # Redirect to home page regardless of the outcome
        return redirect(reverse_lazy('payments_paid'))

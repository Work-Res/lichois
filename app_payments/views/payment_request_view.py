from braces.views import LoginRequiredMixin
from django.shortcuts import render

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from ..forms import TransactionForm
from ..service import CybersourceRequestBuilder


class PaymentRequestView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'cybersource_hosted_checkout/transaction.html'
    form_class = TransactionForm
    success_url = reverse_lazy('payment_receipt')
    success_message = "Your transaction has been completed."

    def post(self, request, document_number, *args, **kwargs):

        builder = CybersourceRequestBuilder(document_number=document_number)
        return render(
            self.request,
            'cybersource_hosted_checkout/post_to_cybersource.html',
            context=builder.to_payment_context(context=self.get_context_data(**kwargs)),
        )
from django.urls import path

from crm_integration.api.views import CrmIncomingFormApplicationRequest

urlpatterns = [
    path(
        "external/crm/forms/receive",
        CrmIncomingFormApplicationRequest.as_view(),
        name="crm_form_submit",
    ),
]

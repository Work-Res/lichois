from django.urls import path

from crm_integration.views.crm_form_submit_view import CRMFormSubmitView

urlpatterns = [
    path("crm/submit/", CRMFormSubmitView.as_view(), name="crm_form_submit"),
]

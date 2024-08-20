from django.urls import path

from .api.views import CRMFormSubmitView

urlpatterns = [
    path("crm/submit", CRMFormSubmitView.as_view(), name="crm_form_submit"),
]

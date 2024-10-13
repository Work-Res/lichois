from django.urls import path

from crm_integration.api.views import WorkResidenceAPIView

urlpatterns = [
    path(
        "work-residence-application/receive",
        WorkResidenceAPIView.as_view(),
        name="work_residence_form_submit",
    ),
]

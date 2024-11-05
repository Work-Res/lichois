from django.urls import path

from .api.views import (
    WorkResidenceAPIView, AppealCrmAPIView, PermitCancellationCrmAPIView,
    EmergencyPermitCrmAPIView, ExemptionCrmAPIView, PrCrmAPIView,
    PrTenYearsCrmAPIView, PermitReplacementCrmAPIView, ResidencePermitCrmAPIView,
    TracelCertificateCrmAPIView, PermitVariationCrmAPIView, VisaCrmAPIView,
    WorkPermitCrmAPIView, BlueCardCrmAPIView)



urlpatterns = [
    path(
        "work-residence-application/receive",
        WorkResidenceAPIView.as_view(),
        name="work_residence_form_submit",
    ),
    path(
        "work-application/receive",
        WorkPermitCrmAPIView.as_view(),
        name="work_form_submit",
    ),
    path(
        "residence-application/receive",
        ResidencePermitCrmAPIView.as_view(),
        name="residence_form_submit",
    ),
    path(
        "appeal/receive",
        AppealCrmAPIView.as_view(),
        name="appeal_form_submit",
    ),
    path(
        "cancellation/receive",
        PermitCancellationCrmAPIView.as_view(),
        name="cancellation_form_submit",
    ),
    path(
        "emergency/receive",
        EmergencyPermitCrmAPIView.as_view(),
        name="emergency_form_submit",
    ),
    path(
        "exemption/receive",
        ExemptionCrmAPIView.as_view(),
        name="exemption_form_submit",
    ),
    path(
        "pr/receive",
        PrCrmAPIView.as_view(),
        name="pr_form_submit",
    ),
    path(
        "pr-ten-years/receive",
        PrTenYearsCrmAPIView.as_view(),
        name="pr_ten_years_form_submit",
    ),
    path(
        "replacement/receive",
        PermitReplacementCrmAPIView.as_view(),
        name="replacement_form_submit",
    ),
    path(
        "travel-certificate/receive",
        TracelCertificateCrmAPIView.as_view(),
        name="travel_certificate_form_submit",
    ),
    path(
        "variation/receive",
        PermitVariationCrmAPIView.as_view(),
        name="variation_form_submit",
    ),
    path(
        "visa/receive",
        VisaCrmAPIView.as_view(),
        name="visa_form_submit",
    ),
    path(
        "blue-card/receive",
        BlueCardCrmAPIView.as_view(),
        name="blue_card_form_submit",
    ),
]

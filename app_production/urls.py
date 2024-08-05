from django.urls import path

from .api.viewsets.production_permit_view import ProductionPermitView


urlpatterns = [
    path(
        "production/<str:document_number>",
        ProductionPermitView.as_view(),
        name="production-permit",
    ),
]

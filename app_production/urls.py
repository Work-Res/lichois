from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api.viewsets.production_attachment_document_viewset import ProductionAttachmentDocumentViewSet
from .api.viewsets.production_permit_view import ProductionPermitView

router = DefaultRouter()
router.register(r'documents', ProductionAttachmentDocumentViewSet)

urlpatterns = [
    path(
        "production/<str:document_number>",
        ProductionPermitView.as_view(),
        name="production-permit",
    ),
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationDocumentListView, ApplicationAttachmentVerificationView

router = DefaultRouter()
router.register(r'attachments', ApplicationDocumentListView)
router.register(r'verifications', ApplicationAttachmentVerificationView)

urlpatterns = [
    path('', include(router.urls)),
]

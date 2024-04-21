from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationDocumentListView

router = DefaultRouter()
router.register(r'attachments', ApplicationDocumentListView)

urlpatterns = [
    path('', include(router.urls)),
]

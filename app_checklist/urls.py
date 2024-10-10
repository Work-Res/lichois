from rest_framework.routers import DefaultRouter

from django.urls import path, include
from .views import (
    ClassifierItemListCreateView,
    ChecklistClassifierItemModelViewSets,
    SystemParameterViewSet,
)

router = DefaultRouter()
router.register(r"classifiers", ClassifierItemListCreateView, basename="classifiers")
router.register(
    r"checklists", ChecklistClassifierItemModelViewSets, basename="checklists"
)
router.register(
    r"system-parameter",
    SystemParameterViewSet,
    basename="system-parameter",
)

urlpatterns = [
    path("", include(router.urls)),
]

from django.urls import path, include

from .views import (
    WorkResidentPermitApplicationDetailView, PermitCreateListView, SpouseCreateListView, ChildCreateListView,
    WorkResidencePermitCreateListView
)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'permits', PermitCreateListView)
router.register(r'spouse', SpouseCreateListView)
router.register(r'child', ChildCreateListView)
router.register(r'workpermitdetails', WorkResidencePermitCreateListView)

urlpatterns = [
    path('workresidentpermit/summary/<str:document_number>', WorkResidentPermitApplicationDetailView.as_view(),
         name='workresidentpermit-detail'),
    path('spouse/<str:document_number>/<str:pk>', SpouseCreateListView.as_view({'get': 'list'}),
         name='spouse-detail'),
    path('', include(router.urls)),
]

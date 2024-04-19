from django.urls import path

from .views import WorkResidentPermitApplicationDetailView

urlpatterns = [
    path('workresidentpermit', WorkResidentPermitApplicationDetailView.as_view(), name='workresidentpermit-detail'),
]

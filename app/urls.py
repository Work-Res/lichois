from django.urls import path
from app.views import ApplicationListView, ApplicationCreateView, ApplicationDetailView

urlpatterns = [
    path('applications', ApplicationCreateView.as_view(), name='application-new'), # new applications
    # path('applications/create/', ApplicationCreateView.as_view(), name='application-create'),
    path('applications/list', ApplicationListView.as_view(), name='application-list'),
    path('applications/detail/<str:document_number>/', ApplicationDetailView.as_view(), name='application-detail'),
]

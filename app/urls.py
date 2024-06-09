from django.urls import path, include

from rest_framework.routers import DefaultRouter

from app.views import (
    ApplicationListView, ApplicationCreateView, ApplicationStatusViewSet, ApplicationVerificationCreateListView,
    ApplicationRenewalView
)


router = DefaultRouter()

router.register(r'applications', ApplicationListView)
router.register(r'application_statuses', ApplicationStatusViewSet)
router.register(r'application_verifications', ApplicationVerificationCreateListView)

urlpatterns = [
    path('applications', ApplicationCreateView.as_view(), name='application-new'),
    path('applications/renewal', ApplicationRenewalView.as_view(), name='application-renewal'),
    path('', include(router.urls)),
]

# urlpatterns = [
#     path('applications', ApplicationCreateView.as_view(), name='application-new'), # new applications
#     # path('applications/create/', ApplicationCreateView.as_view(), name='application-create'),
#     path('applications/list', ApplicationListView.as_view(), name='application-list'),
#     path('applications/detail/<str:document_number>/', ApplicationDetailView.as_view(), name='application-detail'),
# ]

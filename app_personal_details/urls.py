from .views import PersonCreateListView, PassportCreateListView, EducationViewSet, PermitCreateListView

from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'education', EducationViewSet)
router.register(r'permits', PermitCreateListView, basename='permits')
router.register(r'personal_detail/persons', PersonCreateListView, basename="personal_details")


urlpatterns = [
    path('personal_details/passport/<str:document_number>', PassportCreateListView.as_view(), name='create-passport'),
    # path('personal_details/person/<str:document_number>', PersonCreateListView.as_view(), name='create-person'),
    path('', include(router.urls)),
    # path('personal_details/create/', ApplicationCreateView.as_view(), name='application-create'),
    # path('personal_details/<str:created_date>', ApplicationListView.as_view(), name='application-list'),
    # path('personal_details/detail/<str:document_number>/', ApplicationDetailView.as_view(), name='application-detail'),
]

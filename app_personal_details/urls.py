from django.urls import path
from .views import PersonCreateListView, PassportCreateListView


urlpatterns = [
    path('personal_details/passport/<str:document_number>', PassportCreateListView.as_view(), name='create-passport'),
    path('personal_details/person/<str:document_number>', PersonCreateListView.as_view(), name='create-person'),
    # path('personal_details/create/', ApplicationCreateView.as_view(), name='application-create'),
    # path('personal_details/<str:created_date>', ApplicationListView.as_view(), name='application-list'),
    # path('personal_details/detail/<str:document_number>/', ApplicationDetailView.as_view(), name='application-detail'),
]

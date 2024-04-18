from django.urls import path
from .views import ApplicationAttachmentCreateView, ApplicationDocumentListView, ApplicationAttachmentDeleteView

urlpatterns = [
    path('create/', ApplicationAttachmentCreateView.as_view(), name='attachment-create'),
    path('list/', ApplicationDocumentListView.as_view(), name='attachment-list'),
    path('delete/<str:id>/', ApplicationAttachmentDeleteView.as_view(), name='attachment-delete'),
]

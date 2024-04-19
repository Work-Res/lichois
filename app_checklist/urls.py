from django.urls import path
from .views import ClassifierItemListView

urlpatterns = [
    path('checklist/', ClassifierItemListView.as_view(), name='checklist-list'),
]

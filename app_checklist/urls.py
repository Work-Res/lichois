from rest_framework.routers import DefaultRouter

from django.urls import path, include
from .views import ClassifierItemListCreateView, ChecklistClassifierItemModelViewSets

router = DefaultRouter()
router.register(r'classifiers', ClassifierItemListCreateView, basename='classifiers')
router.register(r'checklists', ChecklistClassifierItemModelViewSets, basename='checklists')

urlpatterns = [
    path('', include(router.urls)),
]

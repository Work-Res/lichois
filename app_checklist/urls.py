from rest_framework.routers import DefaultRouter

from django.urls import path, include
from .views import ClassifierItemListCreateView

router = DefaultRouter()
router.register(r'classifiers', ClassifierItemListCreateView, basename='classifiers')

urlpatterns = [
    path('', include(router.urls)),
]

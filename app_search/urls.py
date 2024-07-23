from django.urls import path, include
from rest_framework import routers

from .views import ApplicationVersionSearchView


router = routers.DefaultRouter()
router = routers.DefaultRouter()
router.register(r'applications/search', ApplicationVersionSearchView, basename='applicationversionsearch')


urlpatterns = [
    path("", include(router.urls)),
]

from django.urls import path, include
from rest_framework import routers

from .views import ApplicationVersionSearchView


router = routers.DefaultRouter()
router.register("applications/search", ApplicationVersionSearchView, base_name="application-search")


urlpatterns = [
    path("", include(router.urls)),
]

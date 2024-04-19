from rest_framework import routers

from django.urls import path, include

from .views import ApplicationDecisionViewSet

router = routers.DefaultRouter()
router.register(r'application-decisions', ApplicationDecisionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


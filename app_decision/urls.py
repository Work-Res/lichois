from rest_framework import routers

from django.urls import path, include

from .views import ApplicationDecisionViewSet, ApplicationDecisionTypeViewSet

router = routers.DefaultRouter()
router.register(r'application-decisions', ApplicationDecisionViewSet)
router.register(r'application-decision-types', ApplicationDecisionTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


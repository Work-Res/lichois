from rest_framework import routers

from .views import ApplicationDecisionViewSet

router = routers.DefaultRouter()
router.register(r'application-decisions', ApplicationDecisionViewSet)

urlpatterns = router.urls

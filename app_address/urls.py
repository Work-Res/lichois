from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AddressCreateListView
from .admin_site import address_admin

router = DefaultRouter()
router.register(r'addresses', AddressCreateListView)

urlpatterns = [
    
    path("address/", address_admin.urls),
    path('', include(router.urls)),
]

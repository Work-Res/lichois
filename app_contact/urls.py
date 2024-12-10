"""
URL configuration for comments project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_contact.views import ApplicationContactViewSet
from .admin_site import contact_admin


router = DefaultRouter()
router.register(r'contacts', ApplicationContactViewSet)

urlpatterns = [
    
    path("contact/", contact_admin.urls),
    path('', include(router.urls)),
    path('contacts/<int:document_number>/update_contact/<str:pk>/',
         ApplicationContactViewSet.as_view({'put': 'update_contact'}), name='update-contact'), # Fixme Not working, (ERROR not found)

]

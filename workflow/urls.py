from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskCreateListViewSet

router = DefaultRouter()
router.register(r'tasks', TaskCreateListViewSet, basename='task')

app_name = "workflow"  # Register the 'workflow' namespace

urlpatterns = [
    path('', include(router.urls)),
]
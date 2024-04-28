from .views import TaskCreateListViewSet, TaskSearchAPIView
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'tasks', TaskCreateListViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/search/', TaskSearchAPIView.as_view(), name='task_search')
]

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from workflow.models import Task

from workflow.api.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(group_owner=self.request.user)

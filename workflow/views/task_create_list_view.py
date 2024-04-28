from rest_framework import viewsets
from workflow.models import Task
from ..views import TaskFilter

from workflow.api.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_class = TaskFilter
    ordering_fields = (
        'created',
    )

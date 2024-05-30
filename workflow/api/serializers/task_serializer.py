from rest_framework import serializers
from workflow.models import Task

from app_checklist.api.serializers import ClassifierItemSerializer


from authentication.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):

    office_location = ClassifierItemSerializer()
    assignee = UserSerializer()
    group_owner = UserSerializer()
    participants = UserSerializer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'office_location', 'priority', 'due_date', 'assignee', 'group_owner', 'details', 'participants',
                  'task_notes', 'status']

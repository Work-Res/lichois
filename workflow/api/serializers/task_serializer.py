from rest_framework import serializers
from workflow.models import Task

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TaskSerializer(serializers.ModelSerializer):

    assignee = UserSerializer()
    group_owner = UserSerializer()
    participants = UserSerializer(many=True)

    class Meta:
        model = Task
        fields = ['priority', 'due_date', 'assignee', 'group_owner', 'details', 'participants', 'task_notes', 'status']

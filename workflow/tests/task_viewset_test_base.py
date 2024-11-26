
import os

from rest_framework.test import APITestCase
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from app.classes.permissions import GroupManager
from authentication.models import User
from workflow.models import Task


class TaskViewSetTestBase(APITestCase):
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.other_user = User.objects.create_user(username="otheruser", password="password123")

        content_type = ContentType.objects.get_for_model(Task)

        # Create a group
        permissions = [
            ('wfm_can_assign_task', 'Can assign Task'),
            ('wfm_can_claim_task', 'Can claim Task'),
            ('wfm_can_unassigned_task', 'Can unassigned Task'),
            ('wfm_can_change_task_status', 'Can change Task status')
        ]

        for codename, name in permissions:
            permission = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type
            )

        current_dir = os.path.dirname(__file__)
        group_file_path = os.path.join(current_dir, "data", "groups", "groups.txt")
        manager = GroupManager(group_file_path)

        # Run the create or update groups method
        manager.create_or_update_groups()

        self.group = Group.objects.get(name="Group Tasks")

        for codename, name in permissions:
            permission = Permission.objects.get(
                codename=codename,
                name=name,
                content_type=content_type
            )
            self.group.permissions.add(permission)

        # Add users to the group
        self.user.groups.add(self.group)
        self.other_user.groups.add(self.group)

        self.task = Task.objects.create(
            priority="Low",
            status="NEW",
            details="Test Task",
            assignee=None,
        )
        self.task_in_progress = Task.objects.create(
            priority="High",
            status="IN_PROGRESS",
            details="In Progress Task",
            assignee=self.user,
        )

        # Authenticate the test user
        self.client.force_authenticate(user=self.user)

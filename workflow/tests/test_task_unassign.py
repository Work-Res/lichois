from rest_framework import status
from django.urls import reverse

from .task_viewset_test_base import TaskViewSetTestBase


class TaskUnassignTest(TaskViewSetTestBase):
    def test_unassign_task_success(self):
        self.task.assignee = self.user
        self.task.save()

        # Updated URL name
        url = reverse("workflow:task-unassign", kwargs={"pk": self.task.id})
        response = self.client.post(url)

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Task unassigned successfully.")
        self.assertIsNone(self.task.assignee)

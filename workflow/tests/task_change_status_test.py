from rest_framework import status
from django.urls import reverse

from .task_viewset_test_base import TaskViewSetTestBase


class TaskChangeStatusTest(TaskViewSetTestBase):
    def test_change_status_success(self):
        # Updated URL name
        url = reverse("workflow:task-change-status", kwargs={"pk": self.task.id})
        response = self.client.post(url, {"status": "CLOSED"})

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Task status changed to CLOSED successfully.")
        self.assertEqual(self.task.status, "CLOSED")

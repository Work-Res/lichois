from rest_framework import status
from django.urls import reverse

from .task_viewset_test_base import TaskViewSetTestBase


class TaskChangeStatusTest(TaskViewSetTestBase):
    def test_change_status_success(self):
        url = reverse("task-create-list-viewset-change-status", kwargs={"pk": self.task.id})
        response = self.client.post(url, {"status": "COMPLETED"})

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Task status changed to COMPLETED successfully.")
        self.assertEqual(self.task.status, "COMPLETED")

    def test_change_status_invalid_status(self):
        url = reverse("task-create-list-viewset-change-status", kwargs={"pk": self.task.id})
        response = self.client.post(url, {"status": "INVALID_STATUS"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid status value.")

    def test_change_status_task_not_found(self):
        url = reverse("task-create-list-viewset-change-status", kwargs={"pk": 9999})
        response = self.client.post(url, {"status": "COMPLETED"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Task not found.")

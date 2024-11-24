from rest_framework import status
from django.urls import reverse

from .task_viewset_test_base import TaskViewSetTestBase


class TaskClaimTest(TaskViewSetTestBase):

    def test_claim_task_success(self):
        url = reverse("workflow:task-claim", kwargs={"pk": self.task.id})  # Updated URL name
        response = self.client.post(url)

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Task claimed successfully.")
        self.assertEqual(self.task.assignee, self.user)

    def test_claim_task_success_claim_a_task_already_assigned(self):
        url = reverse("workflow:task-claim", kwargs={"pk": self.task.id})  # Updated URL name
        response = self.client.post(url)

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Task claimed successfully.")
        self.assertEqual(self.task.assignee, self.user)

        self.client.force_authenticate(user=self.other_user)
        url = reverse("workflow:task-claim", kwargs={"pk": self.task.id})  # Updated URL name
        response = self.client.post(url)

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Task claimed successfully.")
        self.assertEqual(self.task.assignee, self.other_user)

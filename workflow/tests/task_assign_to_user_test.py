from .task_viewset_test_base import TaskViewSetTestBase


from django.urls import reverse
from rest_framework import status


class TaskAssignToUserTest(TaskViewSetTestBase):

    def test_assign_to_user_success_with_user_id(self):
        # Updated URL name
        url = reverse("workflow:task-assign-to-user", kwargs={"pk": self.task.id})
        response = self.client.post(url, {"user_id": self.other_user.id})

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], f"Task assigned to {self.other_user.username} successfully.")
        self.assertEqual(self.task.assignee, self.other_user)

    def test_assign_to_user_success_with_username(self):
        url = reverse("workflow:task-assign-to-user", kwargs={"pk": self.task.id})
        response = self.client.post(url, {"username": self.other_user.username})

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], f"Task assigned to {self.other_user.username} successfully.")
        self.assertEqual(self.task.assignee, self.other_user)

    def test_assign_to_user_missing_parameters(self):
        # Updated URL name
        url = reverse("workflow:task-assign-to-user", kwargs={"pk": self.task.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Please provide either user_id or username.")

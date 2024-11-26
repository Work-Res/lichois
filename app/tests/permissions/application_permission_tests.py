from .view_test_base import ViewSetTestBase

from django.urls import reverse
from rest_framework import status


class ApplicationPermissionTests(ViewSetTestBase):

    def test_list_permission(self):
        # Authenticate user without permission
        self.client.force_authenticate(user=self.user_without_permission)
        response = self.client.get(reverse("application-list"))

        # Assert permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticate user with permission
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("application-list"))

        # Assert success
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_permission(self):
        # Authenticate user without permission
        self.client.force_authenticate(user=self.user_without_permission)
        response = self.client.get(reverse("application-detail", kwargs={"pk": self.application.pk}))

        # Assert permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticate user with permission
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("application-detail", kwargs={"pk": self.application.pk}))

        # Assert success
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_permission(self):
        url = reverse("application-list")
        data = {"application_name": "New Application"}

        # Authenticate user without permission
        self.client.force_authenticate(user=self.user_without_permission)
        response = self.client.post(url, data)

        # Assert permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticate user with permission
        self.client.force_authenticate(user=self.user_with_permission)
        response = self.client.post(url, data)

        # Assert success
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_partial_update_permission(self):
        url = reverse("application-detail", kwargs={"pk": self.application.pk})
        data = {"assessment": "Partially Updated Application"}

        # Authenticate user without permission
        self.client.force_authenticate(user=self.user_without_permission)
        response = self.client.patch(url, data)

        # Assert permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticate user with permission
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)

        # Assert success
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_permission(self):
        url = reverse("application-detail", kwargs={"pk": self.application.pk})

        # Authenticate user without permission
        self.client.force_authenticate(user=self.user_without_permission)
        response = self.client.delete(url)

        # Assert permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticate user with permission
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        # Assert success
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

import arrow
import uuid
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import tag
from model_mommy import mommy
from rest_framework.test import APIClient
from rest_framework import status
from ..models import EmergencyResPermitApplication


@pytest.mark.wnr
class EmergencyResPermitApplicationViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password1')

        self.emergency_res_application = mommy.make_recipe(
            'workresidentpermit.emergencyrespermitapplication', )

    @tag('wnr1')
    def test_list(self):
        url = reverse('permits')
        response = self.client.get('url')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = reverse('permits-detail')
        uuid_value = uuid.uuid4()
        permit_data = {'id': uuid_value,}

        response = self.client.post(url, permit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(EmergencyResPermitApplication.objects.filter(id=uuid_value).exists())

    def test_retrieve(self):
        url = reverse('permits-detail')
        response = self.client.get(f'/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment_text'], self.comment.comment_text)

    def test_update(self):
        url = reverse('permits')
        comment_data = {'comment_text': 'This is an updated comment'}
        response = self.client.patch(f'/comments/{self.comment.id}/', comment_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(EmergencyResPermitApplication.objects.get(id=self.comment.id).comment_text, 'This is an updated comment')

    def test_delete(self):
        comment_obj = mommy.make_recipe('comments.comment')
        response = self.client.delete(f'/comments/{comment_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(EmergencyResPermitApplication.objects.filter(id=comment_obj.id).exists())

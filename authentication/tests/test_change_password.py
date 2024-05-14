# tests.py
from django.test import TestCase, Client, tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


from ..mommy_recipe import user_recipe


@tag('test_change_password')
class ChangePasswordViewTest(APITestCase):
    
    def setUp(self):
        self.user = user_recipe.make()
        self.new_password = 'more@123'

    def test_change_password(self):
        response = self.client.post(reverse('change_password'), {
            'old_password': self.user.password,
            'new_password': self.new_password
        })
        print(self.user.password)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.new_password))

from unittest import TestCase
from django.test import tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy.mommy import make
from authentication.recipes import user_recipe


@tag('test_user_registration')
class TestUserRegistration(APITestCase):
	
	def setUp(self):
		self.url = reverse('register')
		self.user = make(user_recipe)
		self.data = {
			'email': self.user.email,
			'username': self.user.username,
			'first_name': self.user.first_name,
			'last_name': self.user.last_name,
			'phone_number': self.user.phone_number,
			'password': 'more@12345',
			'password2': 'more@12345',
		}
	
	@tag('test_valid_user_registration')
	def test_valid_user_registration(self):
		response = self.client.post(self.url, self.data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
	
	@tag('test_invalid_email')
	def test_invalid_email_user_registration(self):
		temp_data = self.data.copy()
		temp_data['email'] = ''
		response = self.client.post(self.url, temp_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data, {'email': ['This field may not be blank.']})
	
	def test_invalid_username_user_registration(self):
		temp_data = self.data.copy()
		temp_data['username'] = ''
		response = self.client.post(self.url, temp_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data, {'username': ['This field may not be blank.']})
	
	def test_invalid_password(self):
		temp_data = self.data.copy()
		temp_data['password'] = '1233'
		response = self.client.post(self.url, temp_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('password', response.data)

	def test_invalid_confirm_password(self):
		temp_data = self.data.copy()
		temp_data['password2'] = '1233@more'
		response = self.client.post(self.url, temp_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('password', response.data)

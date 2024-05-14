from django.test import tag
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


@tag('test_user_login')
class UserLoginTestCase(APITestCase):
	def setUp(self):
		self.url = reverse('token_obtain_pair')
	
	def test_sso_login_valid(self):
		data = {
			'username': 'mmore',
			'password': 'moffat@123'
		}
		response = self.client.post(self.url, data, format='json')
		print(response.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 2)
		
	def test_sso_login_invalid(self):
		data = {
			'username': 'mmore',
			'password': 'moffa@123'
		}
		response = self.client.post(self.url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


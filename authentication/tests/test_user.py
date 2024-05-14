from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class UserTestCase(APITestCase):
	def setUp(self):
		self.url = reverse('user')
	
	def test_get_user_details(self):
		data = {
			'username': 'mmore',
			'password': 'moffat@123'
		}
		response = self.client.post(reverse('login'), data, format='json')
		token = response.data['token']
		headers = {'Authorization': f'Token {token}'}
		response = self.client.get(self.url, format='json', headers=headers)
		print(f'Response: {response.data}')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

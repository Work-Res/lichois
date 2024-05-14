from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class UserLoginTestCase(APITestCase):
	def setUp(self):
		self.url = reverse('logout')
		
		
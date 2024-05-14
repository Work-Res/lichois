# tests.py

from django.test import TestCase, Client, tag
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from ..models import User
from django_otp.plugins.otp_email.models import EmailDevice


@tag('test_email_verification')
class OtpEmailVerificationViewTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = mommy.make(User, username='mmore', email='motlhankamoffat@gmail.com', password='moffat@123')
		self.url = reverse('otp_email_verification')
	
	@tag('test_get_valid_token')
	def test_get_valid_token(self):
		# This test checks if the GET method works correctly. It logs in a user, sends a GET request, and checks if
		self.client.login(username=self.user.username, password=self.user.password)
		
		response = self.client.get(self.url)
		print(response.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['message'], 'sent by email')
		
		device = EmailDevice.objects.get(user=self.user, name='email')
		self.assertIsNotNone(device)
	
	@tag('test_verify_valid_token')
	def test_verify_valid_token(self):
		# This test checks if the POST method works correctly with a valid OTP token.
		self.client.login(username=self.user.username, password=self.user.password)
		
		device, created = EmailDevice.objects.get_or_create(user=self.user, name='email')
		device.generate_challenge()
		token = device.token
		
		response = self.client.post(self.url, {'token': token})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['message'], 'OTP token verified')
	
	def test_verify_invalid_token(self):
		# This test checks if the POST method works correctly with an invalid OTP token.
		self.client.login(username=self.user.username, password=self.user.password)
		device, created = EmailDevice.objects.get_or_create(user=self.user, name='email')
		device.generate_challenge()
		
		response = self.client.post(self.url, {'token': 'invalidtoken'})
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data['error'], 'Invalid token')
	
	def test_get_token_invalid_user(self):
		# This test checks if the GET method works correctly when the user is not found.
		response = self.client.get(self.url)
		print(response.data)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
	
	def test_post_token_invalid_user(self):
		# This test checks if the POST method works correctly when the user is not found.
		self.client.login(username=self.user.username, password=self.user.password)
		response = self.client.post(self.url, {'token': 'anytoken'})
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response.data['error'], 'User not found')
	
	def test_get_token_unauthenticated(self):
		# This test checks if the GET method works correctly when the user is not authenticated.
		self.client.logout()
		
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
	
	def test_verify_token_unauthenticated(self):
		# This test checks if the POST method works correctly when the user is not authenticated.
		self.client.logout()
		
		response = self.client.post(self.url, {'token': 'anytoken'})
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

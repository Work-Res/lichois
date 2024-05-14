# serializers.py
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from rest_framework import serializers
from rest_framework.fields import empty


class PasswordResetSerializer(serializers.Serializer):
	email = serializers.EmailField()
	
	def __init__(self, instance=None, data=empty, **kwargs):
		super().__init__(instance, data, kwargs)
		self.reset_form = None
	
	def validate_email(self, value):
		# Use Django password reset form to validate email
		self.reset_form = PasswordResetForm(data=self.initial_data)
		if not self.reset_form.is_valid():
			raise serializers.ValidationError('Invalid email')
		return value
	
	def save(self):
		request = self.context.get('request')
		# Set some values to trigger the send_email method.
		opts = {
			'use_https': request.is_secure(),
			'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
			'request': request,
		}
		self.reset_form.save(**opts)

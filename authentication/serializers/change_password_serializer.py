# serializers.py
from django.contrib.auth import password_validation
from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
	old_password = serializers.CharField(required=True)
	new_password = serializers.CharField(required=True)
	
	def validate_new_password(self, value):
		password_validation.validate_password(value, self.context.get('user'))
		return value

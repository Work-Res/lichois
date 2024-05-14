from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import User

from django_otp.plugins.otp_email.models import EmailDevice
from rest_framework import status


class OtpEmailVerificationView(APIView):
	def get(self, request):
		user = request.user
		device, created = EmailDevice.objects.get_or_create(user=user, name='email')
		message = device.generate_challenge()
		print(device.token)
		return Response({'message': message}, status=status.HTTP_200_OK)
	
	def post(self, request):
		user = request.user
		token = request.data.get('token')
		try:
			device = EmailDevice.objects.get(user=user, name='email')
		except EmailDevice.DoesNotExist:
			return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
		if not device.verify_token(token):
			return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

		return Response({'message': 'OTP token verified'}, status=status.HTTP_200_OK)
		

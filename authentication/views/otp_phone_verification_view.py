# authentication/views/otp_verification_view.py

from otp_twilio.models import TwilioSMSDevice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import User


class OtpPhoneVerificationView(APIView):
	def get(self, request):
		phone_number = request.user.phone_number
		try:
			user = User.objects.get(phone_number=phone_number)
		except User.DoesNotExist:
			return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
		
		device, created = TwilioSMSDevice.objects.get_or_create(user=user, number=phone_number, name='sms')
		# Send the token to the user's phone number.
		token = device.generate_challenge()
		
		return Response({'message': 'OTP token sent'}, status=status.HTTP_200_OK)
	
	def post(self, request):
		phone_number = request.user.phone_number
		try:
			user = User.objects.get(phone_number=phone_number)
		except User.DoesNotExist:
			return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
		
		token = request.data.get('token')
		device = TwilioSMSDevice.objects.get(user=user, number=phone_number, name='sms')
		if not device.verify_token(token):
			return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
		
		return Response({'message': 'OTP token verified'}, status=status.HTTP_200_OK)

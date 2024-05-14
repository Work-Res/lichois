# authentication/views/otp_token_device_view.py

from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import User


class OtpTokenDeviceView(APIView):
    def get(self, request):
        user = request.user
        device, created = TOTPDevice.objects.get_or_create(user=user, name='default')
        url = device.config_url

        return Response({'url': url}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        token = request.data.get('token')
        device = TOTPDevice.objects.get(user=user, name='default')
        if not device.verify_token(token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'OTP token verified'}, status=status.HTTP_200_OK)
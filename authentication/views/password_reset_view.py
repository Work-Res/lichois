# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import PasswordResetSerializer


class PasswordResetView(APIView):
	def post(self, request, *args, **kwargs):
		serializer = PasswordResetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'status': 'password reset email sent'}, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

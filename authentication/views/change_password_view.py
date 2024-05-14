# views.py
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import ChangePasswordSerializer


class ChangePasswordView(APIView):
	def post(self, request, *args, **kwargs):
		user = request.user
		serializer = ChangePasswordSerializer(data=request.data, context={'user': user})
		if serializer.is_valid():
			old_password = serializer.validated_data.get('old_password')
			if not user.check_password(old_password):
				return Response({"old_password": ["Wrong password."]},
				                status=status.HTTP_400_BAD_REQUEST)
			user.set_password(serializer.validated_data.get('new_password'))
			user.save()
			return Response({'status': 'password changed'}, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

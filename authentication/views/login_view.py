from django.contrib.auth import SESSION_KEY, login
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from ..serializers import UserLoginSerializer
from ..validations import validate_username, validate_password


class LoginVew(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (BasicAuthentication,)
	
	def post(self, request):
		data = request.data
		assert validate_username(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			
			response = Response({
				'groups': list(user.groups.values_list('name', flat=True))
			}, status=status.HTTP_200_OK)
			
			# print(request.session.session_key)
			# response.set_cookie(SESSION_KEY, request.session.session_key)
			return response

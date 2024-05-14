from django.contrib.auth import logout
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutView(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


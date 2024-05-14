from django_roles_access.mixin import RolesMixin
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from ..serializers import UserSerializer


class UserView(RolesMixin, APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (TokenAuthentication, SessionAuthentication, )
	
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)

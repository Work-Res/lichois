from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from authentication.serializers import UserRegisterSerializer


class RegisterView(APIView):
	permission_classes = (permissions.AllowAny,)
	
	def post(self, request):
		data = request.data
		serializer = UserRegisterSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.save()
			return Response({
				'user_id': user.id,
			}, status=status.HTTP_200_OK)


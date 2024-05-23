from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		
		# Add custom claims
		# user roles/groups
		# user general information
		
		token['username'] = user.username
		token['groups'] = list(user.groups.values_list('name', flat=True))
		# ...
		return token

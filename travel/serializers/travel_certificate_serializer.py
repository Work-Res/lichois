from rest_framework import serializers
from ..models import TravelCertificate


class TravelCertificateSerializer(serializers.ModelSerializer):
	class Meta:
		model = TravelCertificate
		fields = '__all__'

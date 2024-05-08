from rest_framework import serializers
from ..models import AdoptedChildRegistration


class AdoptedChildRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptedChildRegistration
        fields = '__all__'

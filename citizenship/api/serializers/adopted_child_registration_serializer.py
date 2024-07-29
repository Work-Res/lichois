from rest_framework import serializers
from citizenship.models import AdoptedChildRegistration


class AdoptedChildRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptedChildRegistration
        fields = '__all__'

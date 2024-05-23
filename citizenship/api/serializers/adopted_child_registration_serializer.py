from rest_framework import serializers
from lichois.citizenship.models import AdoptedChildRegistration


class AdoptedChildRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptedChildRegistration
        fields = '__all__'

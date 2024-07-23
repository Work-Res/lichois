from rest_framework import serializers

from app_oath.models.declarant import Declarant


class DeclarantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declarant
        fields = '__all__'

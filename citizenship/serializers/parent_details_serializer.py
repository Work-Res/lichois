from rest_framework import serializers
from ..models import ParentDetails


class ParentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentDetails
        fields = '__all__'

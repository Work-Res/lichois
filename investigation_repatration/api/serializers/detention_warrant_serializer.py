from rest_framework import serializers
from ...models import DetentionWarrant

class DetentionWarrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetentionWarrant
        fields = '__all__'


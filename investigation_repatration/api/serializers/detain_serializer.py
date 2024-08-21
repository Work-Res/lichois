from rest_framework import serializers
from ...models import Detain

class DetainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detain
        fields = '__all__'


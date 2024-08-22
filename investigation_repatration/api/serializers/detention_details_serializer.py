from rest_framework import serializers
from ...models import DetentionDetails

class DetentionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detain
        fields = '__all__'


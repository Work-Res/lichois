from rest_framework import serializers
from ...models import CommitalWarrent

class CommitalWarrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitalWarrent
        fields = '__all__'


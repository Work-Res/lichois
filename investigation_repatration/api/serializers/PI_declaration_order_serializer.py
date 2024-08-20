from rest_framework import serializers
from ...models import PIDeclarationOrder

class PIDeclarationOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIDeclarationOrder
        fields = '__all__'


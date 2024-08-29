from rest_framework import serializers
from ...models import  PIDeclarationOrderAcknowledgement

class PIDeclarationOrderAcknowledgementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIDeclarationOrderAcknowledgement
        fields = '__all__'

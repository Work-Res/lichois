from rest_framework import serializers
from ...models import PIDeclarationOrder, PIDeclarationOrderAcknowledgement


class PIDeclarationOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIDeclarationOrder
        fields = "__all__"


class PIDeclarationOrderAcknoledgementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIDeclarationOrderAcknowledgement
        fields = "__all__"

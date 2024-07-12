from rest_framework import serializers
from ..models import BoardDecision


class BoardDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardDecision
        fields = "__all__"

from rest_framework import serializers
from ..models import Spouse


class SpouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spouse
        fields = "__all__"

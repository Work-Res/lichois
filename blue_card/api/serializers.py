from rest_framework import serializers
from ..models.blue_card import BlueCard


class BlueCardApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlueCard
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
        extra_kwargs = {
            "status": {"read_only": True},
            "applicant": {"read_only": True},
        }

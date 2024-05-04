from rest_framework import serializers
from ...models import Spouse


class SpouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spouse
        fields = (
            "id",
            "spouse_last_name",
            "spouse_first_name",
            "spouse_middle_name",
            "spouse_maiden_name",
            "spouse_country",
            "spouse_place_birth",
            "spouse_dob",
            "created"
        )

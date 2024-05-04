from rest_framework import serializers
from ...models import PlaceOfResidence, SpousePlaceOfResidence


class PlaceOfResidenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaceOfResidence
        fields = (
            "country",
            "place_of_residence"
        )


class SpousePlaceOfResidenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpousePlaceOfResidence
        fields = (
            "country",
            "place_of_residence"
        )


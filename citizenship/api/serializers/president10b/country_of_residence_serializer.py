from rest_framework import serializers

from citizenship.models import CountryOfResidence


class CountryOfResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryOfResidence
        fields = ['id', 'country', 'period_from', 'period_until']

from rest_framework import serializers

from citizenship.models import CriminalOffense


class CriminalOffenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CriminalOffense
        fields = ['id', 'offense_description', 'date_of_conviction', 'country_of_offense', 'penalty_given']

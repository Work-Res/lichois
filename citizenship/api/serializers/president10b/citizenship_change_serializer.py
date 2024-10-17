from rest_framework import serializers

from citizenship.models import CitizenshipChange


class CitizenshipChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenshipChange
        fields = ['id', 'previous_citizenship', 'new_citizenship', 'date_of_change']

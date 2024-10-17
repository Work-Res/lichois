from rest_framework import serializers

from citizenship.models import ResidencyPeriod


class ResidencyPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidencyPeriod
        fields = ['id', 'period_from', 'period_until', 'country']

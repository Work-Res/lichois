from rest_framework import serializers
from citizenship.models import CitizenshipBySettlement


class CitizenshipBySettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenshipBySettlement
        fields = '__all__'

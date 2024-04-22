from rest_framework import serializers
from ..models import DisposalMoney


class DisposalMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = DisposalMoney
        fields = '__all__'

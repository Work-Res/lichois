from rest_framework import serializers
from lichois.visa.models import DisposalMoney


class DisposalMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = DisposalMoney
        fields = '__all__'

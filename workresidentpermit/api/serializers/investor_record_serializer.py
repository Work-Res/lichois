from rest_framework import serializers

from ...models import InvestorRecord


class InvestorRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestorRecord
        fields = '__all__'

from rest_framework import serializers
from ...models import PIHistory


class PIHistorySerializer(serializers.ModelSerializer):

    detention_reason = serializers.CharField(source='detention_warrant.detention_reason', read_only=True)
    detention_date = serializers.DateField(source='detention_warrant.detention_date', read_only=True)
    reason_for_violation = serializers.CharField(source='penalty.reason_for_violation', read_only=True)
    severity_level = serializers.CharField(source='penalty.severity_level', read_only=True)

    class Meta:
        model = PIHistory
        fields = "__all__"
        read_only_fields = ("non_citizen_identifier", "detention_reason", "detention_date", "reason_for_violation", "severity_level")
        
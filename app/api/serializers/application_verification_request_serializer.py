from rest_framework import serializers


class ApplicationVerificationRequestSerializer(serializers.Serializer):
    decision = serializers.CharField(max_length=200, required=True)
    comment = serializers.CharField(max_length=500, required=False, allow_blank=True)
    outcome_reason = serializers.CharField(
        max_length=300, required=False, allow_blank=True
    )

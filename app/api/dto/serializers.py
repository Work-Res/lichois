from rest_framework import serializers

from .application_verification_request_dto import ApplicationVerificationRequestDTO


class ApplicationVerificationRequestDTOSerializer(serializers.Serializer):
    decision = serializers.CharField(max_length=255, required=False, allow_blank=True)
    comment = serializers.CharField(max_length=255, required=False, allow_blank=True)
    outcome_reason = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def create(self, validated_data):
        return ApplicationVerificationRequestDTO(**validated_data)

    def update(self, instance, validated_data):
        instance.decision = validated_data.get('decision', instance.decision)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.outcome_reason = validated_data.get('outcome_reason', instance.outcome_reason)
        return instance

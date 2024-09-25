from rest_framework import serializers


class ApplicationVerificationRequestSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200, required=True)
    summary = serializers.CharField(max_length=500, required=False, allow_blank=True)
    comment_type = serializers.CharField(max_length=100, required=False, allow_blank=True)

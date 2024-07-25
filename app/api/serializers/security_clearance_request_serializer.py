from rest_framework import serializers


class SecurityClearanceRequestDTOSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200, required=True)
    summary = serializers.CharField(max_length=500, required=False)

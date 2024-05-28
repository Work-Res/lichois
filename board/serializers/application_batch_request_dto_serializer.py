from rest_framework import serializers


class ApplicationBatchRequestDTOSerializer(serializers.Serializer):

    applications = serializers.ListField(
        child=serializers.CharField(max_length=200),
        required=True
    )
    batch_type = serializers.CharField(max_length=200, required=False)

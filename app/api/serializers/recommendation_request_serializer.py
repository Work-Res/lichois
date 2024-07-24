from rest_framework import serializers


class RecommendationRequestDTOSerializer(serializers.Serializer):
    document_number = serializers.CharField(max_length=200, required=True)
    status = serializers.CharField(max_length=200, required=True)
    summary = serializers.CharField(max_length=500, required=False)

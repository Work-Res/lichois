from rest_framework import serializers


class RequestDeferredApplicationDTOSerializer(serializers.Serializer):

    document_number = serializers.CharField(max_length=200, required=True)
    summary = serializers.CharField(max_length=500, required=False)
    comment = serializers.CharField(max_length=500, required=False)
    deferred_from = serializers.CharField(max_length=100, required=False)
    expected_action = serializers.CharField(max_length=100, required=False)
    task_details_config_file = serializers.CharField(max_length=100, required=False)
    batch_id = serializers.CharField(max_length=100, required=False, blank=True)

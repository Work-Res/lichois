from rest_framework import serializers


from ...models.application_replacement_history import ApplicationReplacementHistory


class ApplicationReplacementHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationReplacementHistory
        fields = ("application_type", "comment", "process_name", "historical_record")

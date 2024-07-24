from rest_framework import serializers
from ...models import ApplicationRenewalHistory


class ApplicationRenewalHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationRenewalHistory
        fields = "__all__"

from rest_framework import serializers
from ..models import ApplicationBatch


class ApplicationBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationBatch
        fields = '__all__'

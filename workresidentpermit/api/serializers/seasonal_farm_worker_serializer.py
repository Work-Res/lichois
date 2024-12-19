from rest_framework import serializers

from workresidentpermit.models import SeasonalFarmWorker


class SeasonalFarmWorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = SeasonalFarmWorker
        fields = "__all__"

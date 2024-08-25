from rest_framework import serializers

from app.api.serializers import ApplicationSerializer

from gazette.models import LegalAssessment, BatchApplication, Batch
from gazette.models.batch_decision import BatchDecision


class LegalAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalAssessment
        fields = '__all__'


class BatchApplicationGazetteSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer(read_only=True)

    class Meta:
        model = BatchApplication
        fields = '__all__'


class BatchGazetteSerializer(serializers.ModelSerializer):

    batch_application_count = serializers.SerializerMethodField()

    class Meta:
        model = Batch
        fields = '__all__'

    def get_batch_application_count(self, obj):
        return obj.batch_applications.count()


class BatchDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchDecision
        fields = '__all__'

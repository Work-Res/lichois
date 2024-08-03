from rest_framework import serializers

from app.models import Application
from gazette.models import LegalAssessment, BatchApplication, Batch
from gazette.models.batch_decision import BatchDecision


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class LegalAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalAssessment
        fields = '__all__'


class BatchApplicationSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer(read_only=True)

    class Meta:
        model = BatchApplication
        fields = '__all__'


class BatchGazetteSerializer(serializers.ModelSerializer):
    batch_applications = BatchApplicationSerializer(many=True, read_only=True)
    assessments = LegalAssessmentSerializer(many=True, read_only=True)

    class Meta:
        model = Batch
        fields = '__all__'


class BatchDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchDecision
        fields = '__all__'

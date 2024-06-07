from rest_framework import serializers


from app_checklist.models import Classifier, ClassifierItem, ChecklistClassifierItem, ChecklistClassifier


class ClassifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classifier
        fields = (
            'code',
            'name',
            'description',
            'valid_from',
            'valid_to',
        )


class ClassifierItemSerializer(serializers.ModelSerializer):

    classifier = ClassifierSerializer()

    class Meta:
        model = ClassifierItem
        fields = (
            'code',
            'name',
            'process',
            'description',
            'mandatory',
            'classifier',
            'valid_from',
            'valid_to'
        )


class ChecklistClassifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChecklistClassifier
        fields = (
            'code',
            'name',
            'process_name',
            'description',
            'mandatory',
            'classifier',
            'valid_from',
            'valid_to'
        )


class ChecklistClassifierItemSerializer(serializers.ModelSerializer):

    checklist_classifier = ChecklistClassifierSerializer()

    class Meta:
        model = ChecklistClassifierItem
        fields = (
            'code',
            'name',
            'application_type',
            'description',
            'mandatory',
            'checklist_classifier',
            'valid_from',
            'valid_to'
        )

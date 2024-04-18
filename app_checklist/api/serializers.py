from rest_framework import serializers


from app_checklist.models import Classifier, ClassifierItem


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

from rest_framework import serializers


from ..models import (
    Classifier,
    ClassifierItem,
    ChecklistClassifierItem,
    ChecklistClassifier,
    OfficeLocationClassifierItem,
    OfficeLocationClassifier,
    Location,
    Region,
    SystemParameter,
)


class ClassifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classifier
        fields = (
            "code",
            "name",
            "description",
            "valid_from",
            "valid_to",
        )


class ClassifierItemSerializer(serializers.ModelSerializer):
    classifier = ClassifierSerializer()

    class Meta:
        model = ClassifierItem
        fields = (
            "code",
            "name",
            "process",
            "description",
            "mandatory",
            "classifier",
            "sequence",
            "create_task_rules",
            "valid_from",
            "valid_to",
        )


class ChecklistClassifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistClassifier
        fields = (
            "code",
            "name",
            "process_name",
            "description",
            "valid_from",
            "valid_to",
        )


class ChecklistClassifierItemSerializer(serializers.ModelSerializer):
    checklist_classifier = ChecklistClassifierSerializer()

    class Meta:
        model = ChecklistClassifierItem
        fields = (
            "code",
            "name",
            "application_type",
            "description",
            "mandatory",
            "checklist_classifier",
            "sequence",
            "valid_from",
            "valid_to",
        )


class OfficeLocationClassifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeLocationClassifier
        fields = ("code", "name", "description", "valid_from", "valid_to")


class OfficeLocationClassifierItemSerializer(serializers.ModelSerializer):
    office_location_classifier = OfficeLocationClassifierSerializer()

    class Meta:
        model = OfficeLocationClassifierItem
        fields = (
            "code",
            "name",
            "description",
            "office_location_classifier",
            "valid_from",
            "valid_to",
        )


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = [
            "id",
            "name",
            "code",
            "description",
            "valid_from",
            "valid_to",
            "active",
        ]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class SystemParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemParameter
        fields = "__all__"

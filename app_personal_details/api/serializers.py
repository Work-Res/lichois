from rest_framework import serializers

from app_personal_details.models import (
    Permit,
    Person,
    Passport,
    Education,
    Child,
    Spouse,
    DeceasedSpouseInfo,
    MarriageDissolutionInfo,
)
from app_personal_details.models.name_change import NameChange


class PersonSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        min_length=3, allow_blank=False, trim_whitespace=True, required=True
    )
    last_name = serializers.CharField(
        min_length=3, allow_blank=False, trim_whitespace=True, required=True
    )

    class Meta:
        model = Person
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "maiden_name",
            "marital_status",
            "dob",
            # 'place_birth',
            "gender",
            "occupation",
            "qualification",
            "document_number",
        )
        extra_kwargs = {
            "dob": {"format": "iso-8601"},
        }


class PassportSerializer(serializers.ModelSerializer):
    passport_number = serializers.CharField(
        min_length=3, allow_blank=False, trim_whitespace=True, required=True
    )
    nationality = serializers.CharField(
        min_length=3, allow_blank=False, trim_whitespace=True, required=True
    )

    class Meta:
        model = Passport
        fields = (
            "passport_number",
            "date_issued",
            "place_issued",
            "expiry_date",
            "nationality",
            "document_number",
        )
        extra_kwargs = {
            "date_issued": {"format": "iso-8601"},
            "expiry_date": {"format": "iso-8601"},
        }


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = (
            "id",
            "level",
            "field_of_study",
            "institution",
            "start_date",
            "end_date",
        )


class PermitSerializer(serializers.ModelSerializer):
    place_issue = serializers.CharField(
        min_length=3, allow_blank=False, trim_whitespace=True, required=True
    )
    permit_type = serializers.CharField(
        min_length=3, allow_blank=False, trim_whitespace=True, required=True
    )

    class Meta:
        model = Permit
        fields = (
            "document_number",
            "permit_type",
            "permit_no",
            "date_issued",
            "date_expiry",
            "place_issue",
        )
        extra_kwargs = {
            "date_issued": {"format": "iso-8601"},
            "date_expiry": {"format": "iso-8601"},
        }


class ChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        fields = "__all__"


class SpouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spouse
        fields = "__all__"


class DeceasedSpouseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeceasedSpouseInfo
        fields = ["id", "country_of_death", "place_of_death", "date_of_death"]


class MarriageDissolutionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarriageDissolutionInfo
        fields = [
            "id",
            "country_of_dissolution",
            "place_of_dissolution",
            "date_of_dissolution",
        ]


class NameChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameChange
        fields = ["id", "previous_name", "new_name", "date_of_change"]

from rest_framework import serializers

from app_personal_details.models import Person
from app_address.models import ApplicationAddress
from citizenship.models import FormE


class FormESerializer(serializers.ModelSerializer):

    guardian = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), allow_null=True)
    father = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), allow_null=True)
    mother = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), allow_null=True)
    sponsor = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), allow_null=True)
    witness = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), allow_null=True)

    father_address = serializers.PrimaryKeyRelatedField(queryset=ApplicationAddress.objects.all(), allow_null=True)
    mother_address = serializers.PrimaryKeyRelatedField(queryset=ApplicationAddress.objects.all(), allow_null=True)
    sponsor_address = serializers.PrimaryKeyRelatedField(queryset=ApplicationAddress.objects.all(), allow_null=True)
    witness_address = serializers.PrimaryKeyRelatedField(queryset=ApplicationAddress.objects.all(), allow_null=True)

    class Meta:
        model = FormE
        fields = [
            'id',
            'guardian',
            'citizenship_at_birth',
            'present_citizenship',
            'present_citizenship_not_available',
            'provide_circumstances',
            'father',
            'father_address',
            'mother',
            'mother_address',
            'sponsor',
            'sponsor_address',
            'is_sponsor_signed',
            'sponsor_date_of_signature',
            'witness',
            'witness_address',
        ]

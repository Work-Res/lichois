from rest_framework import serializers

from app_personal_details.models import Person
from app_address.models import ApplicationAddress
from app_checklist.models import Location
from citizenship.models.registration.form_c import FormC


class FormCSerializer(serializers.ModelSerializer):
    # Representing related models by their primary keys
    guardian = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), allow_null=True)
    guardian_address = serializers.PrimaryKeyRelatedField(queryset=ApplicationAddress.objects.all(), allow_null=True)
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), allow_null=True)
    adoptive_parent = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), allow_null=True)
    adoptive_parent_address = serializers.PrimaryKeyRelatedField(queryset=ApplicationAddress.objects.all(), allow_null=True)
    sponsor = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), allow_null=True)
    sponsor_address = serializers.PrimaryKeyRelatedField(queryset=ApplicationAddress.objects.all(), allow_null=True)
    witness = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), allow_null=True)
    witness_address = serializers.PrimaryKeyRelatedField(queryset=ApplicationAddress.objects.all(), allow_null=True)

    class Meta:
        model = FormC
        fields = [
            'id', 'guardian', 'guardian_address', 'location', 'designation',
            'citizenship_at_birth', 'present_citizenship', 'present_citizenship_not_available',
            'provide_circumstances', 'adoptive_parent', 'adoptive_parent_address',
            'sponsor', 'sponsor_address', 'is_sponsor_signed', 'sponsor_date_of_signature',
            'witness', 'witness_address'
        ]

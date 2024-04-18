from rest_framework import serializers

from app_personal_details.models import Permit, Person, Passport


class PersonSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)
    last_name = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)
    application_number = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)

    class Meta:
        model = Person
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'maiden_name',
            'marital_status',
            'dob',
            'place_birth',
            'gender',
            'occupation',
            'qualification',
            'application_number'
        )
        extra_kwargs = {
            'dob': {'format': 'iso-8601'},
        }


class PassportSerializer(serializers.ModelSerializer):

    passport_number = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)
    nationality = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)
    application_number = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)

    class Meta:
        model = Passport
        fields = (
            'passport_number',
            'date_issued',
            'place_issued',
            'expiry_date',
            'nationality',
            'application_number'
        )
        extra_kwargs = {
            'date_issued': {'format': 'iso-8601'},
            'expiry_date': {'format': 'iso-8601'}
        }

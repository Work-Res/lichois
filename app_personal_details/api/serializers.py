from rest_framework import serializers

from app_personal_details.models import Permit, Person, Passport, Education


class PersonSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)
	last_name = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)
	
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
			'document_number'
		)
		extra_kwargs = {
			'dob': {'format': 'iso-8601'},
		}


class PassportSerializer(serializers.ModelSerializer):
	passport_number = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)
	nationality = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)
	
	class Meta:
		model = Passport
		fields = (
			'passport_number',
			'date_issued',
			'place_issued',
			'expiry_date',
			'nationality',
			'document_number',
		)
		extra_kwargs = {
			'date_issued': {'format': 'iso-8601'},
			'expiry_date': {'format': 'iso-8601'}
		}


class EducationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Education
		fields = ('id',
		          'level',
		          'field_of_study',
		          'institution',
		          'start_date',
		          'end_date',)


class PermitSerializer(serializers.ModelSerializer):
	place_issue = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)
	permit_type = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)
	
	class Meta:
		model = Permit
		fields = (
			'permit_type',
			'permit_no',
			'date_issued',
			'date_expiry',
			'place_issue',
		)
		extra_kwargs = {
			'date_issued': {'format': 'iso-8601'},
			'date_expiry': {'format': 'iso-8601'}
		}

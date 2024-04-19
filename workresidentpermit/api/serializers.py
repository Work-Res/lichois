from rest_framework import serializers

from ..models import Permit, Child, Spouse, WorkResidencePermit

from app_personal_details.api.serializers import PersonSerializer, PassportSerializer
from app_address.api.serializers import ApplicationAddressSerializer

from base_module.choices import PREFERRED_METHOD_COMM, YES_NO, REASONS_PERMIT


class PermitSerializer(serializers.ModelSerializer):

    place_issue = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)
    permit_type = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)
    application_number = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)

    class Meta:
        model = Permit
        fields = (
            'permit_type',
            'permit_no',
            'date_issued',
            'date_expiry',
            'place_issue',
            'application_number',
        )
        extra_kwargs = {
            'date_issued': {'format': 'iso-8601'},
            'date_expiry': {'format': 'iso-8601'}
        }


class ChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        fields = (
            "child_first_name",
            "child_last_name",
            "child_age",
            "gender",
            "is_applying_residence"
        )


class SpouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spouse
        fields = (
            "spouse_last_name",
            "spouse_first_name",
            "spouse_middle_name",
            "spouse_country",
            "spouse_place_birth",
            "spouse_dob"
        )


class WorkResidencePermitSerializer(serializers.ModelSerializer):

    file_number = serializers.CharField(required=False)
    preferred_method_comm = serializers.ChoiceField(choices=PREFERRED_METHOD_COMM)
    preferred_method_comm_value = serializers.CharField(required=True)
    language = serializers.CharField()
    permit_reason = serializers.CharField()
    state_period_required = serializers.DateField(required=True)
    propose_work_employment = serializers.ChoiceField(choices=YES_NO)
    reason_applying_permit = serializers.ChoiceField(choices=REASONS_PERMIT)
    documentary_proof = serializers.CharField()
    travelled_on_pass = serializers.CharField()
    is_spouse_applying_residence = serializers.ChoiceField(choices=YES_NO)
    ever_prohibited = serializers.CharField()
    sentenced_before = serializers.CharField()
    entry_place = serializers.CharField()
    arrival_date = serializers.DateField(required=True)

    class Meta:
        model = WorkResidencePermit
        fields = (
            "file_number",
            "preferred_method_comm",
            "preferred_method_comm_value",
            "language",
            "permit_reason",
            "state_period_required",
            "propose_work_employment",
            "reason_applying_permit",
            "documentary_proof",
            "travelled_on_pass",
            "is_spouse_applying_residence",
            "ever_prohibited",
            "sentenced_before",
            "entry_place",
            "arrival_date"
        )


class WorkResidentPermitDataSerializer(serializers.Serializer):
    personal_details = PersonSerializer()
    address = ApplicationAddressSerializer()
    passport = PassportSerializer()
    permit = PermitSerializer()
    child = ChildSerializer()
    spouse = SpouseSerializer()
    form_details = WorkResidencePermitSerializer()


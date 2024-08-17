from rest_framework import serializers
from ...models import ResidencePermit
from base_module.choices import PREFERRED_METHOD_COMM, YES_NO, REASONS_PERMIT


class ResidencePermitSerializer(serializers.ModelSerializer):

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
        model = ResidencePermit
        fields = "__all__"

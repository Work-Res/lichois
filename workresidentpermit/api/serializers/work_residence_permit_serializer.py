from rest_framework import serializers
from ...models import WorkResidencePermit
from base_module.choices import YES_NO, REASONS_PERMIT


class WorkResidencePermitSerializer(serializers.ModelSerializer):

    file_number = serializers.CharField(required=False)
    language = serializers.CharField()
    permit_reason = serializers.CharField()
    previous_nationality = serializers.CharField(required=False)
    current_nationality = serializers.CharField()
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
    arrival_date = serializers.DateField(required=True)

    class Meta:
        model = WorkResidencePermit
        fields = (
            "file_number",
            "language",
            "permit_reason",
            "previous_nationality",
            "current_nationality",
            "state_period_required",
            "propose_work_employment",
            "reason_applying_permit",
            "documentary_proof",
            "travelled_on_pass",
            "is_spouse_applying_residence",
            "ever_prohibited",
            "sentenced_before",
            "entry_place",
            "arrival_date",
        )

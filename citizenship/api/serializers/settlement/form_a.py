from rest_framework import serializers

from citizenship.models import KgosiCertificate, DCCertificate
from citizenship.models.settlement.form_a import FormA
from citizenship.models.settlement.kgosana_certificate import KgosanaCertificate


class FormASerializer(serializers.ModelSerializer):
    # Serialize related objects if necessary
    kgosi_certificate = serializers.PrimaryKeyRelatedField(
        queryset=KgosiCertificate.objects.all(), allow_null=True, required=False
    )
    kgosana_certificate = serializers.PrimaryKeyRelatedField(
        queryset=KgosanaCertificate.objects.all(), allow_null=True, required=False
    )
    dc_certificate = serializers.PrimaryKeyRelatedField(
        queryset=DCCertificate.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = FormA
        fields = [
            'kgosi_certificate',
            'kgosana_certificate',
            'preferred_method_of_comm',
            'dc_certificate',
            'tribe_ordinarily_community_kgosi',
            'tribe_customarily_community_kgosi',
            'tribe_ordinarily_community_kgosana',
            'tribe_customarily_community_kgosana',
        ]

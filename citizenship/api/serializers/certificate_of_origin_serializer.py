from rest_framework import serializers

from app_address.api.serializers import ApplicationAddressSerializer
from app_oath.serializers import DeclarantSerializer, OathDocumentSerializer
from app_personal_details.api import PersonSerializer
from citizenship.api.serializers import KgosiCertificateSerializer, KgosanaCertificateSerializer
from citizenship.models.renunciation import CertificateOfOrigin


class CertificateOfOriginSerializer(serializers.ModelSerializer):

    personal_details = PersonSerializer()
    address = ApplicationAddressSerializer()
    father = PersonSerializer(required=False, allow_null=True)
    mother = PersonSerializer(required=False, allow_null=True)
    kgosi = KgosiCertificateSerializer(required=False, allow_null=True)
    kgosana = KgosanaCertificateSerializer(required=False, allow_null=True)
    declarant = DeclarantSerializer()
    commissioner_of_oath = OathDocumentSerializer()

    class Meta:
        model = CertificateOfOrigin
        fields = '__all__'

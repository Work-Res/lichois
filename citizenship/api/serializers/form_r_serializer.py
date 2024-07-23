from rest_framework import serializers

from app_address.api.serializers import ApplicationAddressSerializer
from app_oath.serializers import DeclarantSerializer, OathDocumentSerializer
from app_personal_details.api import PersonSerializer
from citizenship.models.renunciation import FormR


class FormRSerializer(serializers.ModelSerializer):
    personal_details = PersonSerializer()
    address = ApplicationAddressSerializer()
    declarant = DeclarantSerializer()
    commissioner_of_oath = OathDocumentSerializer()

    class Meta:
        model = FormR
        fields = '__all__'

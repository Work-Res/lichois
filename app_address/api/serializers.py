from app_address.models import Country, ApplicationAddress

from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = (
            'name',
            'iso_code',
            'iso_a2_code',
            'cso_code',
            'local',
            'valid_from',
            'valid_from'
        )


class ApplicationAddressSerializer(serializers.ModelSerializer):

    country = CountrySerializer()

    document_number = serializers.CharField(required=True, allow_blank=False, max_length=100)

    class Meta:
        model = ApplicationAddress
        fields = (
            'apartment_number',
            'plot_number',
            'country',
            'city',
            'street_address',
            'address_type',
            'private_bag',
            'po_box',
            'document_number'
        )

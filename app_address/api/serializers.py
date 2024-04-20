from app_address.models import Country, ApplicationAddress

from rest_framework import serializers

from app.models import ApplicationVersion


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

    class Meta:
        model = ApplicationAddress
        fields = (
            'id',
            'apartment_number',
            'plot_number',
            'country',
            'city',
            'street_address',
            'address_type',
            'private_bag',
            'po_box',
            'document_number',
            'created'
        )

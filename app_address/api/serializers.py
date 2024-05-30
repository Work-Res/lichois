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

    id = serializers.CharField(max_length=100, required=False)

    # def validate(self, data):
    #     cso_code = data.get('country')
    #     try:
    #         country = Country.objects.get(cso_code=cso_code)
    #         serializer = CountrySerializer(country)
    #         data["country"] = serializer.data
    #     except Country.DoesNotExist:
    #         raise
    #     return data

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

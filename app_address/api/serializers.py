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

    country = CountrySerializer()

    document_number = serializers.CharField(required=True, allow_blank=False, max_length=100)

    def validate(self, data):
        if 'document_number' in data:
            try:
                document_number = self.data.get("document_number")
                application_version = ApplicationVersion.objects.get(
                    application__application_document__document_number=document_number)
                data['application_version'] = application_version
            except ApplicationVersion.DoesNotExist:
                raise serializers.ValidationError(f"An application document does not exists with: {document_number}.")
        return data

    @property
    def validated_data(self):
        """
        Returns the validated data after removing a field.
        """
        data = super().validated_data
        # Remove a field from validated data
        if 'document_number' in data:
            del data['document_number']
        return data

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

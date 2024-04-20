from rest_framework import serializers

from app_contact.models import ApplicationContact


class ApplicationContactSerializer(serializers.ModelSerializer):

    document_number = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)

    def validate(self, data):
        contact_type = data.get('contact_type')
        country_code = data.get('country_code')
        if contact_type == 'CELL':
            if country_code is None:
                raise serializers.ValidationError("The country code is required for contact type: CELL.")
        return data

    class Meta:
        model = ApplicationContact
        fields = (
            'id',
            'contact_type',
            'contact_value',
            'description',
            'document_number',
            'country_code',
        )

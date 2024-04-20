from rest_framework import serializers

from app_contact.models import  ApplicationContact


class ApplicationContactSerializer(serializers.ModelSerializer):

    document_number = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)

    class Meta:
        model = ApplicationContact
        fields = (
            'contact_type',
            'contact_value',
            'description'
        )

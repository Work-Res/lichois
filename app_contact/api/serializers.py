from rest_framework import serializers

from app_contact.models import  ApplicationContact


class ApplicationContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationContact
        fields = (
            'contact_type',
            'contact_value',
            'description'
        )

from rest_framework import serializers
from citizenship.models import DeclarationNaturalisationByForeignSpouse
from citizenship.models.residential_history import ResidentialHistory


class ResidentialHistorySerializer(serializers.ModelSerializer):
    """Serializer for ResidentialHistory model."""
    class Meta:
        model = ResidentialHistory
        fields = '__all__'


class DeclarationNaturalisationByForeignSpouseSerializer(serializers.ModelSerializer):
    application_residential_history = ResidentialHistorySerializer(read_only=True)

    class Meta:
        model = DeclarationNaturalisationByForeignSpouse
        fields = [
            'declaration_fname', 'declaration_lname', 'declaration_date',
            'signature', 'declaration_place', 'oath_datetime', 'commissioner_name',
            'commissioner_designation', 'telephone_number', 'commissioner_signature',
            'application_residential_history'
        ]

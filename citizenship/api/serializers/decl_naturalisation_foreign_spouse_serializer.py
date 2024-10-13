from app_personal_details.models.person import Person
from rest_framework import serializers
from citizenship.models import DeclarationNaturalisationByForeignSpouse
from app_address.models.application_address import ApplicationAddress
from app_contact.models.application_contact import ApplicationContact
from citizenship.models.residential_history import ResidentialHistory

class ApplicationAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationAddress
        fields = '__all__'

class ApplicationContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationContact
        fields = '__all__'

class ResidentialHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentialHistory
        fields = '__all__'


class DeclNaturalisationForeignSpouseSerializer(serializers.ModelSerializer):

    application_person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    application_address = ApplicationAddressSerializer()
    application_contact = ApplicationContactSerializer()
    application_residential_history = ResidentialHistorySerializer()

    class Meta:
        model = DeclarationNaturalisationByForeignSpouse
        fields = '__all__'

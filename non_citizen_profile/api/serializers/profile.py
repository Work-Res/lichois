from rest_framework import serializers
from ...models import Address, Biometrics, ContactDetails, Passport, PersonalDetails

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class BiometricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biometrics
        fields = '__all__'

class ContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetails
        fields = '__all__'

class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = '__all__'

class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = '__all__'

class CombinedSerializer(serializers.Serializer):
    address = AddressSerializer()
    biometrics = BiometricsSerializer()
    contact_details = ContactDetailsSerializer()
    passport = PassportSerializer()
    personal_details = PersonalDetailsSerializer()
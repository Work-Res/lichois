from rest_framework import serializers
from app_personal_details.models import (
    Passport,
    Person,
    Education,
    NextOfKin,
)
from ...models import Biometrics
from app_address.models import ApplicationAddress
from app_contact.models import ApplicationContact



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationAddress
        fields = "__all__"


class BiometricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biometrics
        fields = "__all__"


class ContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationContact
        fields = "__all__"


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = "__all__"


class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class NextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
        fields = "__all__"


class CombinedSerializer(serializers.Serializer):
    address = AddressSerializer()
    biometrics = BiometricsSerializer()
    contact_details = ContactDetailsSerializer()
    passport = PassportSerializer()
    personal_details = PersonalDetailsSerializer()
    education = EducationSerializer()
    next_of_kin = NextOfKinSerializer()

    def to_representation(self, instance):
        return {
            "address": AddressSerializer(instance.get("address")).data,
            "biometrics": BiometricsSerializer(instance.get("biometrics")).data,
            "contact_details": ContactDetailsSerializer(
                instance.get("contact_details")
            ).data,
            "passport": PassportSerializer(instance.get("passport")).data,
            "personal_details": PersonalDetailsSerializer(
                instance.get("personal_details")
            ).data,
            "education": EducationSerializer(instance.get("education")).data,
            "next_of_kin": NextOfKinSerializer(instance.get("next_of_kin")).data,
        }

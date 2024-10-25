from rest_framework import serializers

from app_address.api.serializers import ApplicationAddressSerializer
from app_personal_details.api import PersonSerializer, DeceasedSpouseInfoSerializer, MarriageDissolutionInfoSerializer, \
    NameChangeSerializer
from citizenship.api.serializers.president10b import ResidencyPeriodSerializer, LocalLanguageKnowledgeSerializer, \
    CriminalOffenseSerializer, CountryOfResidenceSerializer
from citizenship.models.president10b.form_l import FormL


class FormLSerializer(serializers.ModelSerializer):
    father = PersonSerializer(read_only=True)
    father_address = ApplicationAddressSerializer(read_only=True)
    mother = PersonSerializer(read_only=True)
    mother_address = ApplicationAddressSerializer(read_only=True)
    sponsor = PersonSerializer(read_only=True)
    sponsor_address = ApplicationAddressSerializer(read_only=True)
    witness = PersonSerializer(read_only=True)
    witness_address = ApplicationAddressSerializer(read_only=True)
    deceased_spouse_info = DeceasedSpouseInfoSerializer(read_only=True)
    marriage_dissolution_info = MarriageDissolutionInfoSerializer(read_only=True)
    name_change = NameChangeSerializer(read_only=True)
    residency_periods = ResidencyPeriodSerializer(many=True, read_only=True)
    languages = LocalLanguageKnowledgeSerializer(many=True, read_only=True)
    criminal_offences = CriminalOffenseSerializer(many=True, read_only=True)
    countries_of_residence = CountryOfResidenceSerializer(many=True, read_only=True)



    class Meta:
        model = FormL
        fields = [
            'id', 'residency_periods', 'languages', 'deceased_spouse_info', 'marriage_dissolution_info',
            'father', 'father_address', 'mother', 'mother_address', 'previous_application_date',
            'name_change', 'criminal_offences', 'countries_of_residence', 'relation_description',
            'sponsor', 'sponsor_address', 'witness', 'witness_address', 'citizenship_loss_circumstances'
        ]

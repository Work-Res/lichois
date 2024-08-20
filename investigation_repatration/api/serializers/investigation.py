from rest_framework import serializers
from ...models import CommitalWarrent, NonCitizen, PIDeclarationOrderAcknowledgement, PIDeclarationOrder, PIRecommendation, Prisoner, PrisonerDueRelease


class CommitalWarrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitalWarrent
        fields = '__all__'


class NonCitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonCitizen
        fields = '__all__'

class PIDeclarationOrderAcknowledgementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIDeclarationOrderAcknowledgement
        fields = '__all__'

class PIDeclarationOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIDeclarationOrder
        fields = '__all__'

class PIRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIRecommendation
        fields = '__all__'

class PrisonerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prisoner
        fields = '__all__'

class PrisonerDueReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrisonerDueRelease
        fields = '__all__'
from rest_framework import serializers

from citizenship.models import LocalLanguageKnowledge


class LocalLanguageKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalLanguageKnowledge
        fields = ['id', 'language_name', 'proficiency_level']


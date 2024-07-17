from rest_framework import serializers

from app_oath.models import OathDocument


class OathDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OathDocument
        fields = '__all__'

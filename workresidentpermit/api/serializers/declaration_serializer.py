from rest_framework import serializers

from workresidentpermit.models import Declaration


class DeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declaration
        fields = '__all_'

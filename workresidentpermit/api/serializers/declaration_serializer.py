from rest_framework import serializers

from workresidentpermit.models import Declaration


class DeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declaration
        fields = (
            'declaration_fname',
            'declaration_lname',
            'declaration_date',
            'signature',
        )

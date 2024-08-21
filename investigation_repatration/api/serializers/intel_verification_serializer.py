from rest_framework import serializers
from ...models import IntelVerification

class IntelVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntelVerification
        fields = '__all__'


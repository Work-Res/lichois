from rest_framework import serializers
from ...models import NonCitizen


class NonCitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonCitizen
        fields = '__all__'

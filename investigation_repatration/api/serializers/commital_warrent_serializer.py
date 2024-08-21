from rest_framework import serializers
from ...models import CommittalWarrent

class CommitalWarrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommittalWarrent
        fields = '__all__'


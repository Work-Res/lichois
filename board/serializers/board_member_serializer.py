from rest_framework import serializers
from ..models import BoardMember


class BoardMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMember
        fields = '__all__'

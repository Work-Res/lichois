from rest_framework import serializers
from ...models import AuthorizeDetention

class AuthorizeDetentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorizeDetention
        fields = '__all__'


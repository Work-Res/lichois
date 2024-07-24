from rest_framework import serializers
from .application_serializer import ApplicationSerializer
from ...models import ApplicationVersion


class ApplicationVersionSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer()

    class Meta:
        model = ApplicationVersion
        fields = ("application", "version_number")

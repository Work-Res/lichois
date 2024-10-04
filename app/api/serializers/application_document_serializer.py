from rest_framework import serializers
from .application_user_serializer import ApplicationUserSerializer
from ...models import ApplicationDocument


class ApplicationDocumentSerializer(serializers.ModelSerializer):
    applicant = ApplicationUserSerializer()

    class Meta:
        model = ApplicationDocument
        fields = "__all__"

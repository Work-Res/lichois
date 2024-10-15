from rest_framework import serializers

from ...models import Application
from .application_document_serializer import ApplicationDocumentSerializer
from .application_status_serializer import ApplicationStatusSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    application_status = ApplicationStatusSerializer()
    application_document = ApplicationDocumentSerializer()


    class Meta:
        model = Application
        fields = "__all__"

from rest_framework import serializers

from app_attachments.models import AttachmentDocumentType, ApplicationAttachment


class AttachmentDocumentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttachmentDocumentType
        fields = (
            'id',
            'code',
            'name',
            'valid_from',
            'valid_to',
        )


class ApplicationAttachmentSerializer(serializers.ModelSerializer):

    document_type = AttachmentDocumentTypeSerializer()

    class Meta:
        model = ApplicationAttachment
        fields = (
            'id',
            'filename',
            'storage_object_key',
            'document_url',
            'received_date',
            'document_type',
            'document_number'
        )

from rest_framework import serializers

from app_attachments.models import AttachmentDocumentType, ApplicationAttachment
from ..models import ApplicationAttachmentVerification


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
        

class ApplicationAttachmentVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationAttachmentVerification
        fields = ['id', 'attachment', 'verification_status', 'comment', 'verifier', 'verified_at']

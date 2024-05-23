from rest_framework import serializers

from app_attachments.models import AttachmentDocumentType, ApplicationAttachment
from app_comments.api.serializers import CommentSerializer
from app_comments.models import Comment
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
    
    def to_internal_value(self, data):
        request = self.context.get('request')
        auth_user = request.user
        mutable_data = data.copy()
        mutable_data['verifier'] = auth_user.id
        comment_text = data.get('comment')
        if comment_text:
            comment = Comment.objects.create(user=auth_user, comment_text=comment_text, comment_type='verification')
            mutable_data['comment'] = comment.id
        return super().to_internal_value(mutable_data)
    
    def create(self, validated_data):
        return super().create(validated_data)


from math import e
from rest_framework import serializers

from app_attachments.models import AttachmentDocumentType, ApplicationAttachment
from app_comments.api.serializers import CommentSerializer
from app_comments.models import Comment
from authentication.models import User
from authentication.serializers import UserSerializer
from ..models import ApplicationAttachmentVerification


class AttachmentDocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachmentDocumentType
        fields = (
            "id",
            "code",
            "name",
            "valid_from",
            "valid_to",
        )


class ApplicationAttachmentSerializer(serializers.ModelSerializer):
    document_type = AttachmentDocumentTypeSerializer()

    class Meta:
        model = ApplicationAttachment
        fields = "__all__"

    def create(self, validated_data):
        document_type_data = validated_data.pop("document_type")
        document_type = AttachmentDocumentType.objects.create(**document_type_data)
        application_attachment = ApplicationAttachment.objects.create(
            document_type=document_type, **validated_data
        )
        return application_attachment


class ApplicationAttachmentVerificationSerializer(serializers.ModelSerializer):
    attachment = ApplicationAttachmentSerializer(required=False)
    verifier = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    comment = CommentSerializer(required=False, allow_null=True)

    class Meta:
        model = ApplicationAttachmentVerification
        fields = [
            "id",
            "attachment",
            "verification_status",
            "comment",
            "verifier",
            "verified_at",
        ]

    def to_internal_value(self, data):
        request = self.context.get("request")
        auth_user = request.user
        mutable_data = data.copy()
        mutable_data["verifier"] = auth_user.id
        comment_text = data.get("comment")
        if comment_text:
            mutable_data["comment"] = {
                "comment_text": comment_text,
                "comment_type": "verification",
                "user": auth_user.id,
            }
        else:
            mutable_data["comment"] = None
        return super().to_internal_value(mutable_data)

    def create(self, validated_data):
        attachment_data = validated_data.pop("attachment", None)
        comment_data = validated_data.pop("comment", None)
        if attachment_data:
            attachment_serializer = ApplicationAttachmentSerializer(
                data=attachment_data
            )
            if attachment_serializer.is_valid():
                attachment = attachment_serializer.save()
                validated_data["attachment"] = attachment
            else:
                raise serializers.ValidationError(attachment_serializer.errors)
        if comment_data:
            request = self.context.get("request")
            auth_user = request.user
            comment = Comment.objects.create(
                user=auth_user,
                comment_text=comment_data["comment_text"],
                comment_type=comment_data["verification"],
            )
            validated_data["comment"] = comment
        else:
            validated_data["comment"] = None

        return ApplicationAttachmentVerification.objects.create(**validated_data)

    def update(self, instance, validated_data):
        attachment_data = validated_data.pop("attachment", None)
        comment_data = validated_data.pop("comment", None)

        if attachment_data:
            attachment_serializer = ApplicationAttachmentSerializer(
                instance.attachment, data=attachment_data
            )
            if attachment_serializer.is_valid():
                attachment_serializer.save()
            else:
                raise serializers.ValidationError(attachment_serializer.errors)

        if comment_data:
            request = self.context.get("request")
            auth_user = request.user
            if instance.comment:
                instance.comment.comment_text = comment_data.get(
                    "comment_text", instance.comment.comment_text
                )
                instance.comment.save()
            else:
                comment = Comment.objects.create(
                    user=auth_user,
                    comment_text=comment_data["comment_text"],
                    comment_type="verification",
                )
                instance.comment = comment

        instance.verification_status = validated_data.get(
            "verification_status", instance.verification_status
        )
        instance.verified_at = validated_data.get("verified_at", instance.verified_at)
        instance.save()

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["verifier"] = UserSerializer(instance.verifier).data
        return representation

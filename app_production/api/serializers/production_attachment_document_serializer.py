from rest_framework import serializers

from app_production.models import ProductionAttachmentDocument


class ProductionAttachmentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionAttachmentDocument
        fields = ['id', 'document_type', 'document_number', 'pdf_document']

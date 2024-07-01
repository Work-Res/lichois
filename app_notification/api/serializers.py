from rest_framework import serializers
from ..models import Notification
from django.contrib.contenttypes.models import ContentType


class NotificationSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(slug_field='model', queryset=ContentType.objects.all())
    # content_object = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = '__all__'

    def get_content_object(self, obj):
        # Customize this method to serialize related content_object data if needed
        return str(obj.content_object)

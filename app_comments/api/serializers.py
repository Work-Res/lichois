from re import U
from rest_framework import serializers

from authentication.serializers.user_serializer import UserSerializer
from authentication.models import User
from ..models import Comment


class CommentSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Comment
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = UserSerializer(instance.user).data
        return representation

    # def to_internal_value(self, data):
    #     user_data = data.get("user")
    #     if isinstance(user_data, dict):
    #         user_id = user_data.get("id")
    #         if user_id:
    #             data["user"] = user_id
    #         else:
    #             raise serializers.ValidationError(
    #                 {"user": "User dictionary must contain 'id' key."}
    #             )
    #     elif not isinstance(user_data, int):
    #         raise serializers.ValidationError(
    #             {"user": "Expected a dictionary or an integer."}
    #         )
    #     return super().to_internal_value(data)

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from app.api.common.web import APIMessage
from ..models import BoardMember, VotingProcess


class VotingProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotingProcess
        fields = (
            "board",
            "status",
            "batch",
            "board_meeting",
        )

    def to_internal_value(self, data):
        request = self.context.get("request")
        auth_user = request.user
        board_member = BoardMember.objects.filter(user=auth_user).first()
        if not board_member:
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details="User is not a member of any board",
            )
            raise PermissionDenied(api_message.to_dict())
        mutable_data = data.copy()
        mutable_data["board"] = board_member.board.id
        return super().to_internal_value(mutable_data)

    def create(self, validated_data):
        return super().create(validated_data)

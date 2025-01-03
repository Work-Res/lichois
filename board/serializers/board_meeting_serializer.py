from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from app.api.common.web import APIMessage
from ..models import BoardMeeting, BoardMember

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BoardMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMeeting
        fields = (
            "id",
            "title",
            "meeting_date",
            "description",
            "status",
            "minutes",
            "meeting_type",
            "location",
            "board",
            "meeting_start_time",
            "meeting_end_time",
        )

    def to_internal_value(self, data):
        request = self.context.get("request")
        auth_user = request.user
        board_member = BoardMember.objects.filter(user=auth_user).first()
        if not board_member:
            logger.error(f"User is not a member of any board {auth_user}")
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details=f"User {auth_user} is not a member of any board",
            )
            raise PermissionDenied(api_message.to_dict())
        # if data is dict, it is immutable, so we need to make a mutable copy
        if isinstance(data, dict):
            mutable_data = data.copy()
            mutable_data["board"] = board_member.board.id
            return super().to_internal_value(mutable_data)
        return super().to_internal_value(data)

    def create(self, validated_data):
        return super().create(validated_data)

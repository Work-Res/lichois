from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from app.api.common.web import APIMessage
from ..choices import PRESENT
from ..models import BoardMember, InterestDeclaration, MeetingAttendee


class InterestDeclarationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InterestDeclaration
        fields = (
            'id',
            'meeting_attendee',
            'document_number',
            'client_relationship',
            'interest_description',
            'decision',
            'attendee_signature',
            'date_signed',
        )
        
    def to_internal_value(self, data):
        request = self.context.get('request')
        auth_user = request.user
        mutable_data = data.copy()
        board_member = BoardMember.objects.filter(user=auth_user).first()
        if not board_member:
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details="User is not a member of any board"
            )
            raise PermissionDenied(api_message.to_dict())
        try:
            meeting_attendee = MeetingAttendee.objects.get(Q(board_member=board_member) & Q(
                attendance_status=PRESENT))
        except MeetingAttendee.DoesNotExist:
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details="Board member is not an attendee of the meeting or absent"
            )
            raise PermissionDenied(api_message.to_dict())
        else:
            mutable_data['meeting_attendee'] = meeting_attendee.id
        return super().to_internal_value(mutable_data)
    
    def create(self, validated_data):
        return super().create(validated_data)
        

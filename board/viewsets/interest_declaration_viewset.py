from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.api.common.web import APIMessage
from ..choices import PRESENT, ABSENT
from ..models import BoardMember, InterestDeclaration, MeetingAttendee
from ..serializers import InterestDeclarationSerializer


class InterestDeclarationViewSet(viewsets.ModelViewSet):
    queryset = InterestDeclaration.objects.all()
    serializer_class = InterestDeclarationSerializer

    @action(
        detail=False,
        methods=['get'],
        url_path='current-attendee/(?P<document_number>[A-Za-z0-9-]+)/(?P<meeting>[A-Za-z0-9-]+)',
        url_name='current-attendee')
    def check_interest_declaration(self, request, document_number, meeting):
        board_member = BoardMember.objects.filter(user=request.user).first()
        if not board_member:
            return Response(APIMessage(message='User is not a member of any board', code=400).to_dict())
        meeting_attendee = MeetingAttendee.objects.filter(
            board_member=board_member,
            attendance_status=PRESENT,
            meeting=meeting).first()
        if not meeting_attendee:
            return Response(APIMessage(message='User is not an attendee of board meeting', code=400).to_dict())
        interest_declaration = InterestDeclaration.objects.filter(meeting_attendee=meeting_attendee,
                                                                  document_number=document_number).first()
        if interest_declaration:
            return Response(data=InterestDeclarationSerializer(interest_declaration).data)
        return Response(APIMessage(message='Interest declaration not found', code=404).to_dict(), status=404)

    @action(
        detail=False,
        methods=['get'],
        url_path='interest-declarations/(?P<document_number>[A-Za-z0-9-]+)/(?P<meeting>[A-Za-z0-9-]+)',
        url_name='interest-declarations')
    def interest_declarations(self, request, document_number, meeting):
        board_member = BoardMember.objects.filter(user=request.user).first()
        if not board_member:
            return Response(APIMessage(message='User is not a member of any board', code=400).to_dict())

        interest_declarations = InterestDeclaration.objects.filter(
            decision='refrain', document_number=document_number, meeting__id=meeting)
        if interest_declarations:
            return Response(data=InterestDeclarationSerializer(interest_declarations, many=True).data)
        return Response(APIMessage(message='Interest declaration not found', code=404).to_dict(), status=404)

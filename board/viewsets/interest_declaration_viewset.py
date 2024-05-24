from rest_framework import viewsets
from rest_framework.response import Response

from app.api.common.web import APIMessage
from ..models import BoardMember, InterestDeclaration
from ..serializers import InterestDeclarationSerializer


class InterestDeclarationViewSet(viewsets.ModelViewSet):
	queryset = InterestDeclaration.objects.all()
	serializer_class = InterestDeclarationSerializer
	
	# def create(self, request, *args, **kwargs):
	# 	# if interest declaration exists, raise an error
	# 	document_number = request.data.get('document_number')
	# 	board_member = BoardMember.objects.filter(user=request.user).first()
	# 	if not board_member:
	# 		return Response(APIMessage(message='User is not a member of any board', code=400).to_dict())
	# 	meting_attendee = MeetingAttendee.objects.filter(Q(board_member=board_member) & Q(attendance_status=PRESENT) & Q(meeting=request.data.get('meeting'))).first()
	# 	if InterestDeclaration.objects.filter(document_number=document_number).exists():
	# 		return Response(APIMessage(message='Interest declaration already exists', code=500).to_dict())
	# 	return super().create(request, *args, **kwargs)

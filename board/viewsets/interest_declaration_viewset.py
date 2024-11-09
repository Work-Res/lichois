from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.api.common.web import APIMessage
from app.models import Application
from ..choices import PRESENT, ABSENT
from ..models import BoardMember, InterestDeclaration, MeetingAttendee
from ..serializers import InterestDeclarationSerializer


class InterestDeclarationViewSet(viewsets.ModelViewSet):
    queryset = InterestDeclaration.objects.all()
    serializer_class = InterestDeclarationSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="current-attendee/(?P<document_number>[A-Za-z0-9-]+)/(?P<meeting>[A-Za-z0-9-]+)",
        url_name="current-attendee",
    )
    def check_interest_declaration(self, request, document_number, meeting):
        board_member = BoardMember.objects.filter(user=request.user).first()
        if not board_member:
            return Response(
                APIMessage(
                    message="User is not a member of any board", code=400
                ).to_dict()
            )
        meeting_attendee = MeetingAttendee.objects.filter(
            board_member=board_member, attendance_status=PRESENT, meeting=meeting
        ).first()
        if not meeting_attendee:
            return Response(
                APIMessage(
                    message="User is not an attendee of board meeting", code=400
                ).to_dict(),
                status=400,
            )
        interest_declaration = InterestDeclaration.objects.filter(
            meeting_attendee=meeting_attendee, document_number=document_number
        ).first()
        if interest_declaration:
            return Response(
                data=InterestDeclarationSerializer(interest_declaration).data
            )
        return Response(
            APIMessage(message="Interest declaration not found", code=404).to_dict(),
            status=404,
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="participants/refrained/(?P<document_number>[A-Za-z0-9-]+)/(?P<meeting>[A-Za-z0-9-]+)",
        url_name="interest-declarations-refrain",
    )
    def interest_declarations_refrained(self, request, document_number, meeting):
        board_member = BoardMember.objects.filter(user=request.user).first()
        if not board_member:
            return Response(
                APIMessage(
                    message="User is not a member of any board", code=400
                ).to_dict()
            )

        interest_declarations = InterestDeclaration.objects.filter(
            decision="refrain", document_number=document_number, meeting__id=meeting
        )
        if interest_declarations:
            return Response(
                data=InterestDeclarationSerializer(
                    interest_declarations, many=True
                ).data
            )
        return Response(
            APIMessage(message="Interest declaration not found", code=404).to_dict(),
            status=404,
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="participants/vote/(?P<document_number>[A-Za-z0-9-]+)/(?P<meeting>[A-Za-z0-9-]+)",
        url_name="interest-declarations-vote",
    )
    def interest_declarations_voting(self, request, document_number, meeting):
        board_member = BoardMember.objects.filter(user=request.user).first()
        if not board_member:
            return Response(
                APIMessage(
                    message="User is not a member of any board", code=400
                ).to_dict()
            )

        interest_declarations = InterestDeclaration.objects.filter(
            decision="vote", document_number=document_number, meeting__id=meeting
        )
        if interest_declarations:
            return Response(
                data=InterestDeclarationSerializer(
                    interest_declarations, many=True
                ).data
            )
        return Response(
            APIMessage(message="Interest declaration not found", code=404).to_dict(),
            status=404,
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="create-batch",
        url_name="create-batch",
    )
    def create_interest_declaration_no_conflict(self, request):

        batch = request.data.get("batch", None)
        meeting = request.data.get("meeting", None)
        if not batch:
            return Response(APIMessage(message="Batch is required", code=400).to_dict())

        for pk in batch:
            application = Application.objects.filter(pk=pk).first()
            if not application:
                return Response(
                    APIMessage(
                        message=f"Application with id {pk} not found", code=404
                    ).to_dict(),
                    status=404,
                )
            interest_declaration = InterestDeclaration.objects.filter(
                document_number=application.application_document.document_number,
            ).first()
            if not interest_declaration:
                data = {
                    "document_number": application.application_document.document_number,
                    "meeting": meeting,
                    "decision": "vote",
                    "attendee_signature": True,
                }
                serializer = self.get_serializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    self.perform_create(serializer)

        return Response(
            APIMessage(
                message="Interest declaration batch created successfully",
                code=201,
                details={"batch": batch},
            ).to_dict(),
            status=201,
        )

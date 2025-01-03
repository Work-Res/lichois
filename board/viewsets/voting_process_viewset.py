from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from app.api.common.web import APIMessage
from app.api.common.web.api_response import APIResponse
from board.models.application_batch import ApplicationBatch

from ..models import VotingProcess
from ..serializers import VotingProcessSerializer


class VotingProcessViewSet(viewsets.ModelViewSet):
    queryset = VotingProcess.objects.all()
    serializer_class = VotingProcessSerializer
    lookup_field = "document_number"

    def create(self, request, *args, **kwargs):
        if not request.user.is_chairperson():
            api_message = APIMessage(
                code=403,
                message="Forbidden",
                details="Only the chairperson can create a voting process.",
            )
            raise PermissionDenied(api_message.to_dict())

        voting_process = VotingProcess.objects.filter(
            document_number=request.data.get("document_number")
        ).first()
        if voting_process:
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details="Voting process already exists.",
            )
            raise PermissionDenied(api_message.to_dict())
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=["post"], url_path="batch-create")
    def create_batch(self, request, *args, **kwargs):
        if not request.user.is_chairperson():
            api_message = APIMessage(
                code=403,
                message="Forbidden",
                details="Only the chairperson can create voting processes in batch.",
            )
            raise PermissionDenied(api_message.to_dict())

        application_batch = request.data.get("application_batch", None)
        voting_status = request.data.get("status", None)
        board_meeting = request.data.get("board_meeting", None)
        created_processes = []
        if not application_batch or not status or not board_meeting:
            api_message = APIMessage(
                code=400,
                message="Bad request",
                details="application_batch, status and board_meeting are required fields.",
            )
            raise PermissionDenied(api_message.to_dict())

        batch = ApplicationBatch.objects.filter(id=application_batch).first()
        if not batch:
            api_message = APIMessage(
                code=404,
                message="Not found",
                details="Application batch not found.",
            )
            raise PermissionDenied(api_message.to_dict())
        for app in batch.applications.all():
            # check first if voting process already exists
            voting_process = VotingProcess.objects.filter(
                document_number=app.application_document.document_number
            ).first()
            if not voting_process:
                data = {
                    "document_number": app.application_document.document_number,
                    "status": voting_status,
                    "board_meeting": board_meeting,
                }
                serializer = self.get_serializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    self.perform_create(serializer)
                    created_processes.append(serializer.data)

        return Response(
            APIResponse(
                messages=f"Successfully created voting process for batch {application_batch}",
                data=created_processes,
                status=201,
            ).result(),
            status=status.HTTP_201_CREATED,
        )

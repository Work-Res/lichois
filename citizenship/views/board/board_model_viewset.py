from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from citizenship.api.serializers.board import BoardSerializer, MeetingSerializer
from citizenship.models.board import Board, Meeting, Role
from citizenship.service.board.board_service import BoardService


class BoardModelViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quorum_roles = Role.objects.filter(id__in=request.data.get('quorum_roles', []))
        board = BoardService.create_board(
            name=serializer.validated_data['name'],
            description=serializer.validated_data['description'],
            quorum_roles=quorum_roles
        )
        return Response(BoardSerializer(board).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def update_board(self, request, pk=None):
        board_id = pk
        name = request.data.get('name')
        description = request.data.get('description')
        quorum_roles = Role.objects.filter(id__in=request.data.get('quorum_roles', []))
        try:
            board = BoardService.update_board(board_id=board_id, name=name, description=description, quorum_roles=quorum_roles)
            return Response(BoardSerializer(board).data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_meeting(self, request, pk=None):
        board_id = pk
        title = request.data.get('title')
        location = request.data.get('location')
        agenda = request.data.get('agenda')
        status = request.data.get('status', 'Scheduled')
        try:
            meeting = BoardService.add_board_meeting(board_id=board_id, title=title, location=location, agenda=agenda, status=status)
            return Response(MeetingSerializer(meeting).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

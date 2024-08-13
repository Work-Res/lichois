from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.core.exceptions import ValidationError

from app.api.common.pagination import StandardResultsSetPagination
from citizenship.api.serializers.board import BoardSerializer, MeetingSerializer

from citizenship.models import Board
from citizenship.service.board.board_service import BoardService
from citizenship.views.board.filter import BoardFilter


class BoardModelViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filterset_class = BoardFilter
    pagination_class = StandardResultsSetPagination

    def create(self, request):
        name = request.data.get('name')
        region_id = request.data.get('region_id')
        description = request.data.get('description')
        quorum_role_ids = request.data.get('quorum_role_ids', [])
        try:
            board = BoardService.create_board(name, region_id, description, quorum_role_ids)
            serializer = BoardSerializer(board)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_board(self, request, pk=None):
        name = request.data.get('name')
        region_id = request.data.get('region_id')
        description = request.data.get('description')
        quorum_role_ids = request.data.get('quorum_role_ids')
        try:
            board = BoardService.update_board(pk, name, region_id, description, quorum_role_ids)
            serializer = BoardSerializer(board)
            return Response(serializer.data)
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

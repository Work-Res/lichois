from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from citizenship.api.serializers.board import BoardMemberCitizenshipSerializer
from citizenship.models import BoardMember
from citizenship.views.board.filter import BoardMemberFilter


class BoardMemberViewSet(viewsets.ModelViewSet):
    queryset = BoardMember.objects.all()
    serializer_class = BoardMemberCitizenshipSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BoardMemberFilter

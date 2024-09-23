from rest_framework import viewsets, status
from django.core.exceptions import ValidationError
from rest_framework.response import Response

from citizenship.api.serializers.board import BoardRecommendationSerializer
from citizenship.models import BoardRecommendation
from citizenship.service.board.board_recommendation_service import (
    BoardRecommendationService,
)
from django_filters.rest_framework import DjangoFilterBackend

from .filter.board_recommandation_filter import BoardRecommendationFilter


class BoardRecommendationViewSet(viewsets.ModelViewSet):
    queryset = BoardRecommendation.objects.all()
    serializer_class = BoardRecommendationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BoardRecommendationFilter

    def create(self, request):
        document_number = request.data.get("document_number")
        recommendation = request.data.get("recommendation")
        reason = request.data.get("reason", "")
        try:
            board_recommendation = (
                BoardRecommendationService.create_board_recommendation(
                    document_number, recommendation, reason
                )
            )
            serializer = BoardRecommendationSerializer(board_recommendation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

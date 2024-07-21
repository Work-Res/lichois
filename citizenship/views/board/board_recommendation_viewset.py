from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from citizenship.api.serializers.board import BoardRecommendationSerializer
from citizenship.models.board.board_recommandation import BoardRecommendation
from citizenship.service.board.board_recommendation_service import BoardRecommendationService


class BoardRecommendationViewSet(viewsets.ViewSet):
    def list(self, request):
        board_recommendations = BoardRecommendation.objects.all()
        serializer = BoardRecommendationSerializer(board_recommendations, many=True)
        return Response(serializer.data)

    def create(self, request):
        score_sheet_id = request.data.get('score_sheet_id')
        recommendation = request.data.get('recommendation')
        reason = request.data.get('reason', '')
        try:
            board_recommendation = BoardRecommendationService.create_board_recommendation(score_sheet_id, recommendation, reason)
            serializer = BoardRecommendationSerializer(board_recommendation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            board_recommendation = BoardRecommendationService.get(pk)
            serializer = BoardRecommendationSerializer(board_recommendation)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        recommendation = request.data.get('recommendation')
        reason = request.data.get('reason')
        try:
            board_recommendation = BoardRecommendationService.update(pk, recommendation, reason)
            serializer = BoardRecommendationSerializer(board_recommendation)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            BoardRecommendationService.delete(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError

from citizenship.api.serializers.board import ScoreSheetSerializer
from citizenship.models.board import ScoreSheet
from citizenship.service.board.score_sheet_service import ScoreSheetService


class ScoreSheetViewSet(viewsets.ModelViewSet):
    queryset = ScoreSheet.objects.all()
    serializer_class = ScoreSheetSerializer

    def create(self, request, *args, **kwargs):
        try:
            interview_id = request.data.get('interview')
            total_score = request.data.get('total_score')
            aggregated_responses = request.data.get('aggregated_responses')
            passed = request.data.get('passed')
            summary = request.data.get('summary')

            score_sheet = ScoreSheetService.create_score_sheet(
                interview_id=interview_id,
                total_score=total_score,
                aggregated_responses=aggregated_responses,
                passed=passed,
                summary=summary
            )

            serializer = self.get_serializer(score_sheet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': 'An error occurred while creating the score sheet.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        try:
            score_sheet_details = ScoreSheetService.list_score_sheet_details(pk)
            return Response(score_sheet_details, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': 'An error occurred while fetching the score sheet details.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

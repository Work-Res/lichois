from rest_framework import viewsets, status
from rest_framework.response import Response

from django.core.exceptions import ValidationError

from citizenship.api.serializers.board import InterviewDecisionSerializer
from citizenship.models import InterviewDecision
from citizenship.service.board import InterviewDecisionService


class DecisionViewSet(viewsets.ViewSet):
    def list(self, request):
        decisions = InterviewDecision.objects.all()
        serializer = InterviewDecisionSerializer(decisions, many=True)
        return Response(serializer.data)

    def create(self, request):
        interview_id = request.data.get('interview_id')
        member_id = request.data.get('member_id')
        passed = request.data.get('passed')
        reason = request.data.get('reason', '')
        try:
            decision = InterviewDecisionService.create_decision(interview_id, member_id, passed, reason)
            serializer = InterviewDecisionSerializer(decision)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            decision = InterviewDecisionService.get_decision(pk)
            serializer = InterviewDecisionSerializer(decision)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        passed = request.data.get('passed')
        reason = request.data.get('reason')
        try:
            decision = InterviewDecisionService.update_decision(pk, passed, reason)
            serializer = InterviewDecisionSerializer(decision)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            InterviewDecisionService.delete_decision(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

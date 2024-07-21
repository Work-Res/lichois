from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from citizenship.api.serializers.board import InterviewQuestionSerializer
from citizenship.models.board import InterviewQuestion
from citizenship.service.board import InterviewQuestionService


class InterviewQuestionViewSet(viewsets.ViewSet):
    def list(self, request):
        interview_questions = InterviewQuestion.objects.all()
        serializer = InterviewQuestionSerializer(interview_questions, many=True)
        return Response(serializer.data)

    def create(self, request):
        interview_id = request.data.get('interview_id')
        question_text = request.data.get('question_text')
        score = request.data.get('score')
        member_id = request.data.get('member_id')
        comments = request.data.get('comments', '')
        is_marked = request.data.get('is_marked', False)
        try:
            interview_question = InterviewQuestionService.create_interview_question(
                interview_id, question_text, score, member_id, comments, is_marked)
            serializer = InterviewQuestionSerializer(interview_question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            interview_question = InterviewQuestionService.get_interview_question(pk)
            serializer = InterviewQuestionSerializer(interview_question)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        question_text = request.data.get('question_text')
        score = request.data.get('score')
        comments = request.data.get('comments')
        is_marked = request.data.get('is_marked')
        try:
            interview_question = InterviewQuestionService.update_interview_question(
                pk, question_text, score, comments, is_marked)
            serializer = InterviewQuestionSerializer(interview_question)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            InterviewQuestionService.delete_interview_question(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from citizenship.models.board import Question
from citizenship.serializers import QuestionSerializer
from citizenship.services.question_service import QuestionService


class QuestionViewSet(viewsets.ViewSet):
    def list(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def create(self, request):
        text = request.data.get('text')
        try:
            question = QuestionService.create_question(text)
            serializer = QuestionSerializer(question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            question = QuestionService.get_question(pk)
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        text = request.data.get('text')
        try:
            question = QuestionService.update_question(pk, text)
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            QuestionService.delete_question(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
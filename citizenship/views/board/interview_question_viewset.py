import csv

import logging

from rest_framework.decorators import action

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from citizenship.api.serializers.board import InterviewQuestionSerializer, InterviewQuestionCSVSerializer
from citizenship.models.board import Meeting
from citizenship.service.board import InterviewQuestionService

logger = logging.getLogger(__name__)


class InterviewQuestionViewSet(viewsets.ViewSet):
    def list(self, request):
        meeting_id = request.query_params.get('meeting_id')
        if not meeting_id:
            return Response({'detail': 'Meeting ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            questions = InterviewQuestionService.list_interview_questions(meeting_id)
            serializer = InterviewQuestionSerializer(questions, many=True)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            question = InterviewQuestionService.get_interview_question(pk)
            serializer = InterviewQuestionSerializer(question)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        meeting_id = request.data.get('meeting_id')
        text = request.data.get('text')
        if not meeting_id or not text:
            return Response({'detail': 'Meeting ID and text are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            question = InterviewQuestionService.create_interview_question(meeting_id, text)
            serializer = InterviewQuestionSerializer(question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        text = request.data.get('text')
        if not text:
            return Response({'detail': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            question = InterviewQuestionService.update_interview_question(pk, text)
            serializer = InterviewQuestionSerializer(question)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            InterviewQuestionService.delete_interview_question(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='upload-csv')
    def upload_csv(self, request):
        serializer = InterviewQuestionCSVSerializer(data=request.data)
        if serializer.is_valid():
            csv_file = serializer.validated_data['csv_file']
            meeting_id = request.data.get('meeting_id')
            if not meeting_id:
                return Response({'detail': 'Meeting ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                meeting = Meeting.objects.get(id=meeting_id)
            except Meeting.DoesNotExist:
                return Response({'detail': 'Meeting does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            next(reader)  # Skip the header row

            questions_created = 0
            for row in reader:
                text = row[0]
                try:
                    InterviewQuestionService.create_interview_question(meeting.id, text)
                    questions_created += 1
                except ValidationError as e:
                    logger.error(f"Error creating interview question: {str(e)}")

            return Response({'detail': f'{questions_created} questions created successfully.'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

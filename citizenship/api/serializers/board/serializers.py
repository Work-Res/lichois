from rest_framework import serializers


from citizenship.models import Meeting, Attendee, Batch, BatchApplication, Board, Question, Interview, \
    InterviewDecision, ScoreSheet, Role
from citizenship.models.board.board_recommandation import BoardRecommendation
from citizenship.models.board.interview_question import InterviewQuestion
from citizenship.models.board.meeting_session import MeetingSession


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingSession
        fields = '__all__'


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = '__all__'


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'


class BatchApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchApplication
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class InterviewQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = InterviewQuestion
        fields = '__all__'


class InterviewSerializer(serializers.ModelSerializer):
    questions = InterviewQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Interview
        fields = '__all__'


class InterviewDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewDecision
        fields = '__all__'


class ScoreSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreSheet
        fields = '__all__'


class BoardRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardRecommendation
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class InterviewQuestionCSVSerializer(serializers.Serializer):
    csv_file = serializers.FileField()


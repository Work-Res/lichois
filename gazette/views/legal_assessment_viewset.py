# views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from app.models import Application
from gazette.api.serializers.serializers import LegalAssessmentSerializer
from gazette.models import LegalAssessment
from gazette.service.legal_assessment_service import LegalAssessmentService


class LegalAssessmentViewSet(viewsets.ModelViewSet):
    queryset = LegalAssessment.objects.all()
    serializer_class = LegalAssessmentSerializer

    def create(self, request, *args, **kwargs):
        application_id = request.data.get('application_id')
        assessment_text = request.data.get('assessment_text')
        legal_member_id = request.user.id
        try:
            application = Application.objects.get(id=application_id)
            if LegalAssessment.objects.filter(application=application).exists():
                raise ValidationError("A LegalAssessment for this application already exists.")

            legal_assessment = LegalAssessmentService.create_assessment(
                application_id, legal_member_id, assessment_text)
            serializer = self.get_serializer(legal_assessment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        assessment_text = request.data.get('assessment_text')
        try:
            legal_assessment = LegalAssessmentService.update_assessment(instance.id, assessment_text)
            serializer = self.get_serializer(legal_assessment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

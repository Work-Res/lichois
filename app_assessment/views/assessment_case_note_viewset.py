import logging

from rest_framework import viewsets
from django.db import transaction, IntegrityError
from rest_framework.response import Response
from rest_framework import status

from app_assessment.api.serializers import AssessmentCaseNoteSerializer
from app_assessment.models import AssessmentCaseNote
from app_assessment.views.filters import AssessmentCaseNoteFilter


class AssessmentCaseNoteViewSet(viewsets.ModelViewSet):

    queryset = AssessmentCaseNote.objects.all()
    serializer_class = AssessmentCaseNoteSerializer
    filterset_class = AssessmentCaseNoteFilter
    logger = logging.getLogger(__name__)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        self.logger.info(f"Updating case note {instance.parent_object_id} with data: {request.data}")
        try:
            with transaction.atomic():
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                self.logger.info(f"Case note {instance.parent_object_id} updated successfully")
                return Response(serializer.data)
        except IntegrityError as ex:
            self.logger.error(f"Transaction failed and was rolled back. {ex}")
            return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        except AssessmentCaseNote.DoesNotExist:
            self.logger.error(f"Case note with ID {instance.parent_object_id} does not exist.")
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

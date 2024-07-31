from rest_framework import viewsets, status
from rest_framework.response import Response

from gazette.api.serializers.serializers import BatchSerializer
from gazette.models import Batch
from gazette.service import ApplicationBatchService
from gazette.service.batch_decision_service import BatchDecisionService


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        description = request.data.get('description')
        created_by = request.user.id
        batch = ApplicationBatchService.create_batch(title, description, created_by)
        serializer = self.get_serializer(batch)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def add_application(self, request, pk=None):
        batch_id = pk
        application_id = request.data.get('application_id')
        ApplicationBatchService.add_application_to_batch(batch_id, application_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def add_applications(self, request, pk=None):
        batch_id = pk
        application_ids = request.data.get('application_ids', [])
        ApplicationBatchService.add_applications_to_batch(batch_id, application_ids)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def remove_application(self, request, pk=None):
        batch_id = pk
        application_id = request.data.get('application_id')
        ApplicationBatchService.remove_application_from_batch(batch_id, application_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def submit_batch(self, request, pk=None):
        batch_id = pk
        ApplicationBatchService.submit_batch(batch_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create_batch_decision(self, request, pk=None):
        batch_id = pk
        legal_member_id = request.user.id
        decision = request.data.get('decision')
        comments = request.data.get('comments')
        BatchDecisionService.create_batch_decision(batch_id, legal_member_id, decision, comments)
        return Response(status=status.HTTP_201_CREATED)

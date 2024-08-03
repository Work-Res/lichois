from rest_framework import viewsets, status
from rest_framework.response import Response

from gazette.api.serializers.serializers import BatchGazetteSerializer
from gazette.models import Batch, BatchApplication
from gazette.service import BatchSubmissionService


class BatchSubmissionViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchGazetteSerializer

    def submit_batch(self, request, pk=None):
        try:
            batch_id = pk
            if not BatchApplication.objects.filter(batch_id=batch_id).exists():
                return Response({"detail": "Cannot submit batch with no applications."},
                                status=status.HTTP_400_BAD_REQUEST)

            BatchSubmissionService.submit_batch(batch_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update_batch_status(self, request, pk=None):
        try:
            batch_id = pk
            status = request.data.get('status')
            BatchSubmissionService.update_batch_status(batch_id, status)
            return Response(status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

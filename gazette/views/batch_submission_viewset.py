from rest_framework import viewsets, status
from rest_framework.response import Response

from gazette.api.serializers.serializers import BatchGazetteSerializer
from gazette.models import Batch, BatchApplication
from ..service.batch_submission_service import BatchSubmissionService


class BatchSubmissionViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling batch submissions.

    Methods:
    - submit_batch: Submits a batch with the given ID.
    - update_batch_status: Updates the status of a batch with the given ID.

    Attributes:
    - queryset: Queryset containing all Batch objects.
    - serializer_class: Serializer class for BatchGazetteSerializer.
    """

    queryset = Batch.objects.all()
    serializer_class = BatchGazetteSerializer

    def submit_batch(self, request, pk=None):
        try:
            batch_id = pk
            if not BatchApplication.objects.filter(batch_id=batch_id).exists():
                return Response(
                    {"detail": "Cannot submit batch with no applications."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            BatchSubmissionService.submit_batch(batch_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update_batch_status(self, request, pk=None):
        try:
            batch_id = pk
            _status = request.data.get("status")
            BatchSubmissionService.update_batch_status(batch_id, _status)
            return Response(status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

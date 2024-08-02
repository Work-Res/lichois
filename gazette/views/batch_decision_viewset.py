from rest_framework import viewsets, status
from rest_framework.response import Response

from gazette.api.serializers.serializers import BatchDecisionSerializer
from gazette.models import Batch
from gazette.models.batch_decision import BatchDecision
from gazette.service.batch_decision_service import BatchDecisionService


class BatchDecisionViewSet(viewsets.ModelViewSet):

    queryset = BatchDecision.objects.all()
    serializer_class = BatchDecisionSerializer

    def create(self, request, *args, **kwargs):
        batch_id = request.data.get('batch_id')
        decision = request.data.get('decision')
        comments = request.data.get('comments')
        legal_member_id = request.user.id

        try:
            batch = Batch.objects.get(id=batch_id)
            print(batch.__dict__)
            if batch.status != "RECOMMENDED":
                return Response({"detail": "Only batches with RECOMMENDED status can be approved."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Batch.DoesNotExist:
            return Response({"detail": "Batch not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            batch_decision = BatchDecisionService.create_batch_decision(batch_id, legal_member_id, decision, comments)
            serializer = self.get_serializer(batch_decision)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

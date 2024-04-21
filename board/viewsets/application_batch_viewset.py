from rest_framework import viewsets
from ..models import ApplicationBatch
from ..serializers import ApplicationBatchSerializer


class ApplicationBatchViewSet(viewsets.ModelViewSet):
	queryset = ApplicationBatch.objects.all()
	serializer_class = ApplicationBatchSerializer

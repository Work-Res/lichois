from rest_framework import viewsets
from ..models import ApplicationBatch
from ..serializers import ApplicationBatchSerializer


class ApplicationBatchViewSet(viewsets.ModelViewSet):
	queryset = ApplicationBatch.objects.all()
	serializer_class = ApplicationBatchSerializer
	
	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		for application in instance.applications.all():
			application.batched = False
			application.save()
		return super().destroy(request, *args, **kwargs)

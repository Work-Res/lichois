from rest_framework import viewsets
from ..models import ResidencePermitCancellation
from ..api.serializers import ResidencePermitCancellationSerializer


class ResidencePermitCancellationViewSet(viewsets.ModelViewSet):
	queryset = ResidencePermitCancellation.objects.all()
	serializer_class = ResidencePermitCancellationSerializer

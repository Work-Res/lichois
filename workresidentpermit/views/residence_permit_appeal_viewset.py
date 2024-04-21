from rest_framework import viewsets
from ..models import ResidencePermitAppeal
from ..api.serializers import ResidencePermitAppealSerializer


class ResidencePermitAppealViewSet(viewsets.ModelViewSet):
	queryset = ResidencePermitAppeal.objects.all()
	serializer_class = ResidencePermitAppealSerializer

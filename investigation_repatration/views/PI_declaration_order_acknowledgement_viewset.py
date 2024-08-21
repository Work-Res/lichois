from rest_framework import viewsets
from ..models import PIDeclarationOrderAcknowledgement
from api.serializers import PIDeclarationOrderAcknowledgementSerializer


class PIDeclarationOrderAcknowledgementViewSet(viewsets.ModelViewSet):
    queryset = PIDeclarationOrderAcknowledgement.objects.all()
    serializer_class = PIDeclarationOrderAcknowledgementSerializer

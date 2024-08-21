from rest_framework import viewsets
from ..models import CommitalWarrent
from api.serializers import CommitalWarrentSerializer

class CommitalWarrentViewSet(viewsets.ModelViewSet):
    queryset = CommitalWarrent.objects.all()
    serializer_class = CommitalWarrentSerializer
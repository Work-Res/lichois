from rest_framework import viewsets
from ..models import CommittalWarrent
from ..api.serializers import CommitalWarrentSerializer


class CommitalWarrentViewSet(viewsets.ModelViewSet):
    queryset = CommittalWarrent.objects.all()
    serializer_class = CommitalWarrentSerializer

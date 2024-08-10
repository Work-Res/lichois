from rest_framework import viewsets
from rest_framework.response import Response

from base_module.models import Spouse
from base_module.serializers import SpouseSerializer


class SpouseCreateListView(viewsets.ModelViewSet):
    queryset = Spouse.objects.all()
    serializer_class = SpouseSerializer

    def list(self, request, document_number, *args, **kwargs):
        queryset = Spouse.objects.filter(
            work_resident_permit__document_number=document_number
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

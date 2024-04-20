from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Permit
from ..api.serializers import PermitSerializer


class PermitCreateListView(viewsets.ModelViewSet):
    queryset = Permit.objects.all()
    serializer_class = PermitSerializer

    def list(self, request, document_number, *args, **kwargs):
        queryset = Permit.objects.filter(work_resident_permit__document_number=document_number)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

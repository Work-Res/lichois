from rest_framework import viewsets
from rest_framework.response import Response

from base_module.models import Child
from base_module.serializers import ChildSerializer


class ChildCreateListView(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

    def list(self, request, document_number, *args, **kwargs):
        queryset = Child.objects.filter(
            work_resident_permit__document_number=document_number
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

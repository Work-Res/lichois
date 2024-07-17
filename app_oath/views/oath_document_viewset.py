from rest_framework import viewsets

from app_oath.models import OathDocument
from app_oath.serializers import OathDocumentSerializer


class OathDocumentViewSet(viewsets.ModelViewSet):
    queryset = OathDocument.objects.all()
    serializer_class = OathDocumentSerializer


from rest_framework import viewsets

from citizenship.api.serializers import FormRSerializer
from citizenship.models.renunciation import FormR


class FormRViewSet(viewsets.ModelViewSet):
    queryset = FormR.objects.all()
    serializer_class = FormRSerializer
    lookup_field = 'document_number'
